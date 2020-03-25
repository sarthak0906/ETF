import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ
sys.path.extend(['/home/piyush/Desktop/etf/ETFAnalysis', '/home/piyush/Desktop/etf/ETFAnalysis/ETFsList_Scripts',
                 '/home/piyush/Desktop/etf/ETFAnalysis/HoldingsDataScripts',
                 '/home/piyush/Desktop/etf/ETFAnalysis/CalculateETFArbitrage',
                 '/home/piyush/Desktop/etf/ETFAnalysis/PolygonTickData'])
import pandas as pd
import logging
import asyncio
from PolygonTickData.helper import Helper
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig(filename="Test2Logs.log", format='%(asctime)s %(message)s')


class RunArbitrage(object):

    def __init__(self,etfname=None):
        self.tradePricesDF=None
        self.quotesSpreadsDf=None
        
        
    def giveArbitrageResults(self,tradeData=None,quotesData=None,priceforNAVfilling=None):
        helperObj = Helper()
        # Convert tickHistDataQuotes to dict
        #tradeData = helperObj.convertDictToFrame(tickHistDataTrade)
        #tradeData = tradeData[['Symbol', 'p', 's', 't', 'x']]
        tradeData = tradeData[tradeData['s'] != 0]
        # Convert tickHistDataQuotes to dict
        #quotesData = helperObj.convertDictToFrame(tickHistDataQuotes)
        #quotesData = quotesData[['Symbol', 'P', 'S', 'p', 's', 't', 'x', 'X']]
        quotesData = quotesData[quotesData['S'] != 0]
        quotesData = quotesData[quotesData['s'] != 0]
        #########**************#########
        # Needs Threading in time conversion #
        #########**************#########
        tradeData['t'] = tradeData['t'].apply(lambda x: helperObj.getHumanTime(x))
        quotesData['t'] = quotesData['t'].apply(lambda x: helperObj.getHumanTime(x))
        quotesData['Spread'] = quotesData['P'] - quotesData['p']
        quotesData['MidPrice'] = (quotesData['P'] + quotesData['p']) / 2
        # Group Trade Data by minutes
        tradePricesDFMinutes = tradeData.groupby([tradeData['t'].dt.hour, tradeData['t'].dt.minute, tradeData['Symbol']])['p'].mean()
        tradePricesDFMinutes = tradePricesDFMinutes.unstack(level=2)
        tradePricesDFMinutes = tradePricesDFMinutes.fillna(method='ffill')
        self.tradePricesDFMinutes = tradePricesDFMinutes.fillna(priceforNAVfilling)
        # Group Quotes Data by minutes
        quotesSpreadsMinutes = quotesData.groupby([quotesData['t'].dt.hour, quotesData['t'].dt.minute, quotesData['Symbol']])['Spread'].mean()
        quotesSpreadsMinutes = quotesSpreadsMinutes.unstack(level=2)
        self.quotesSpreadsMinutes = quotesSpreadsMinutes.fillna(0)

        self.quotesSpreadsMinutes.to_csv("quotesByMinutes.csv")
        self.tradePricesDFMinutes.to_csv("tradesByMinutes.csv")

        self.tradeData=tradeData
        self.quotesData=quotesData


    def getMeHourdata(self, getmeHourDataFor=None,etfData=None,tradePricesDFMinutes=None, quotesSpreadsMinutes=None):
        etfspread = quotesSpreadsMinutes[self.etfname]
        for name, group in tradePricesDFMinutes.groupby(level=0):
            if name == getmeHourDataFor:
                break
        etfprice = group[self.etfname]
        del group[self.etfname]
        group = group.pct_change().dropna() * 100
        etfpricechange = etfprice.pct_change().dropna() * 100
        etfpricechange = etfpricechange.unstack(level=1)
        netassetvaluereturn = group.assign(**etfData.getETFWeights()).mul(group).sum(axis=1)
        netassetvaluereturn = netassetvaluereturn.unstack(level=1)
        ds = pd.concat([etfprice.unstack(level=1), etfpricechange, netassetvaluereturn], axis=0).T
        ds.columns = ['ETF Price', 'ETF Change Price %', 'Net Asset Value Change%']
        ds['Arbitrage in $'] = (ds['ETF Change Price %'] - ds['Net Asset Value Change%']) * ds['ETF Price'] / 100
        ds['ETF Trading Spread in $'] = etfspread.unstack(level=1).loc[getmeHourDataFor]
        return ds


if __name__ == "__main__":
    date = '2020-03-13'
    etfname = 'XLK'

    etfData = LoadHoldingsdata().LoadHoldingsAndClean(etfname=etfname, fundholdingsdate='20200226')
    print(dir(etfData))
    print(etfData.getSymbols())
    print(etfData.getETFWeights())
    print(etfData.getCashValue())

    polygonApi=CallPolygonApi(date=date)
    tradePricesDF, quotesSpreadDF, priceforNAVfilling =polygonApi.assemblePolygonData(etfData.getSymbols())

    runArbitrageObject=RunArbitrage(etfname=etfname)
    runArbitrageObject.giveArbitrageResults(tradeData=tradePricesDF,quotesData=quotesSpreadDF,priceforNAVfilling=priceforNAVfilling)
    
    for i in range(9, 16):
        print("Hour at=" + str(i))
        try:
            res = runArbitrageObject.getMeHourdata(getmeHourDataFor=i,etfData=etfData,
                tradePricesDFMinutes=runArbitrageObject.tradePricesDFMinutes, 
                quotesSpreadsMinutes=runArbitrageObject.quotesSpreadsMinutes)

            res['Arbitrage in $'] = abs(res['Arbitrage in $'])
            res['Flag'] = 0
            res.loc[(res['Arbitrage in $'] > res['ETF Trading Spread in $']) & res['ETF Trading Spread in $'] != 0, 'Flag'] = 111
            print(res)
        except KeyError:
            print("No Spread data was found for the ETF in this hour")
