'''
Id:          "$Id$"
Copyright:   Copyright (c) 2020 Bank of America Merrill Lynch, All Rights Reserved
Description:
Test:
'''

import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ
sys.path.extend(['/home/piyush/Desktop/etf/ETFAnalysis', '/home/piyush/Desktop/etf/ETFAnalysis/ETFsList_Scripts',
                 '/home/piyush/Desktop/etf/ETFAnalysis/HoldingsDataScripts',
                 '/home/piyush/Desktop/etf/ETFAnalysis/CalculateETFArbitrage',
                 '/home/piyush/Desktop/etf/ETFAnalysis/PolygonTickData'])
import pandas as pd
import logging
import asyncio
from PolygonTickData.PolygonDataAPIConnection import PolgonData
from CalculateETFArbitrage.helper import Helper

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig(filename="Test2Logs.log", format='%(asctime)s %(message)s')


class EtfData(object):
    __slots__ = ('symbol', 'data')

    def __init__(self, sybl, dt):
        self.symbol = sybl
        self.data = dt


class LoadHoldingsdata(object):

    def __init__(self, ticker='XLK', date='20200226'):
        self.cashvalueweight, self.weights, self.symbols = '', '', ''
        try:
            holdings = Helper().getHoldingsDatafromDB(ticker, date)
            holdings['TickerWeight'] = holdings['TickerWeight'] / 100
            # Assign cashvalueweight 
            self.cashvalueweight = holdings[holdings['TickerSymbol'] == 'CASH'].get('TickerWeight').item()

            # Assign Weight %
            self.weights = dict(zip(holdings.TickerSymbol, holdings.TickerWeight))

            # Assign symbols
            symbols = holdings['TickerSymbol'].tolist()
            symbols.append(ticker)
            symbols.remove('CASH')
            self.symbols = symbols

            log.info("Data Successfully Loaded")

        except Exception as e:
            log.error("Data NOT Loaded")
            logging.critical(e, exc_info=True)

    '''    
    @classmethod
    def getETFWeights(cls):
        return self.weights
    
    @classmethod    
    def getCashValue(cls):
        return self.cashvalueweight
    
    @classmethod
    def getSymbols(cls):
        return self.symbols
    '''

    @property
    def getETFWeights(self):
        return self.weights

    @property
    def getCashValue(self):
        return self.cashvalueweight

    @property
    def getSymbols(self):
        return self.symbols


class RunArbitrage(object):

    def __init__(self, date=None, previousdate=None, starttime='9:00:00', endtime='17:00:00', endtimeLoop='16:00:00',
                 etfticker=None):
        self.helperObj = Helper()
        self.date = date
        self.starttime = starttime  # 9 AM
        self.endtime = endtime  # 5 PM
        self.endtimeLoop = endtimeLoop  # 4 PM
        self.extractDataTillTime = self.helperObj.stringTimeToDatetime(date=self.date, time=self.endtimeLoop)
        self.marketTimeStamps = self.helperObj.convertStringDateToTS(date=self.date, starttime=self.starttime,
                                                                     endtime=self.endtime)
        self.etfticker = etfticker
        self.etfholdingsdata = []

    async def getDataFromPolygon(self, symbol=None, getMethodForPolygon=None):
        data = getMethodForPolygon(date=self.date, symbol=symbol, endTS=self.marketTimeStamps['marketCloseTS'],
                                   limitresult=str(50000))
        lastUnixTimeStamp = self.getLastTimeStamp(data)
        await asyncio.sleep(0.2)

        # Check for Pagination
        while self.checkTimeStampForPagination(lastUnixTimeStamp):
            paginatedData = getMethodForPolygon(date=self.date, symbol=symbol, startTS=str(lastUnixTimeStamp),
                                                endTS=self.marketTimeStamps['marketCloseTS'], limitresult=str(50000))
            lastUnixTimeStamp = self.getLastTimeStamp(paginatedData)
            data['results'].extend(paginatedData['results'])
            # print(data)
        dataobject = EtfData(symbol, data)
        del data
        # Creating a slot object
        return dataobject

    def getLastTimeStamp(self, data):
        return data['results'][-1]['t']

    def checkTimeStampForPagination(self, checkTime):
        return True if self.helperObj.getHumanTime(checkTime) < self.extractDataTillTime else False

    def runHistoricalArbitrageCalculations(self):
        etfData = LoadHoldingsdata()
        print(etfData.getSymbols)
        print(etfData.getETFWeights)
        print(etfData.getCashValue)

        tickHistDataQuotes = []
        tickHistDataTrade = []
        priceforNAVfilling = {}

        Polygonobj = PolgonData()

        # Async to get data from Polygon Starts here
        async def main_():
            async def one_iter(semaphore_, symbol):
                async with semaphore_:
                    tickHistDataQuotes.append(await self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricQuotes))
                    tickHistDataTrade.append(await self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricTrades))
                    opencloseDf = Polygonobj.PolygonDailyOpenClose(date=date, symbol=symbol)
                    priceforNAVfilling[symbol] = opencloseDf['open']

            semaphore = asyncio.BoundedSemaphore(4)
            co_routines = [one_iter(semaphore, symbol) for symbol in etfData.getSymbols]
            # co_routines = [one_iter(semaphore, symbol) for symbol in ['AAPL','MSFT','XLK']]
            await asyncio.gather(*co_routines)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main_())
        '''
        helperObj = Helper()
        # Convert tickHistDataQuotes to dict
        tradeData = helperObj.convertDictToFrame(tickHistDataTrade)
        tradeData = tradeData[['Symbol', 'p', 's', 't', 'x']]
        tradeData = tradeData[tradeData['s'] != 0]
        
        # Convert tickHistDataQuotes to dict
        quotesData = helperObj.convertDictToFrame(tickHistDataQuotes)
        quotesData = quotesData[['Symbol', 'P', 'S', 'p', 's', 't', 'x', 'X']]
        quotesData = quotesData[quotesData['S'] != 0]
        quotesData = quotesData[quotesData['s'] != 0]

        # Deleting to save space on disk
        del tickHistDataTrade
        del tickHistDataQuotes

        #########**************#########
        # Needs Threading in time conversion #
        #########**************#########
        # tradeData['t'] = tradeData['t'].apply(lambda x: helperObj.getHumanTimeNew(x))
        # quotesData['t'] = quotesData['t'].apply(lambda x: helperObj.getHumanTimeNew(x))
        #
        # quotesData['Spread'] = quotesData['P'] - quotesData['p']
        # quotesData['MidPrice'] = (quotesData['P'] + quotesData['p']) / 2
        #
        # # Group Trade Data by minutes
        # tradePrices = tradeData.groupby([tradeData['t'].dt.hour, tradeData['t'].dt.minute, tradeData['Symbol']])[
        #     'p'].mean()
        # tradePricesDF = tradePrices.unstack(level=2)
        # tradePricesDF = tradePricesDF.fillna(method='ffill')
        # tradePricesDF = tradePricesDF.fillna(priceforNAVfilling)
        #
        # # Group Quotes Data by minutes
        # quotesSpreads = quotesData.groupby([quotesData['t'].dt.hour, quotesData['t'].dt.minute, quotesData['Symbol']])[
        #     'Spread'].mean()
        # quotesSpreadDF = quotesSpreads.unstack(level=2)
        # quotesSpreadDF = quotesSpreadDF.fillna(0)

        
        '''
        tradePricesDF = pd.DataFrame()
        quotesSpreadDF = pd.DataFrame()
        return tradePricesDF, quotesSpreadDF

    def getMeHourdata(self, getmeHourDataFor=None, tradePricesDF=None, quotesSpreadDF=None):

        etfspread = quotesSpreadDF[self.etfticker]

        for name, group in tradePricesDF.groupby(level=0):
            if name == getmeHourDataFor:
                break

        etfprice = group[etfticker]
        del group[etfticker]

        group = group.pct_change().dropna() * 100

        etfpricechange = etfprice.pct_change().dropna() * 100
        etfpricechange = etfpricechange.unstack(level=1)

        netassetvaluereturn = group.assign(**self.etfholdingsdata['weights']).mul(group).sum(axis=1)
        netassetvaluereturn = netassetvaluereturn.unstack(level=1)

        ds = pd.concat([etfprice.unstack(level=1), etfpricechange, netassetvaluereturn], axis=0).T
        ds.columns = ['ETF Price', 'ETF Change Price %', 'Net Asset Value Change%']

        ds['Arbitrage in $'] = (ds['ETF Change Price %'] - ds['Net Asset Value Change%']) * ds['ETF Price'] / 100
        ds['ETF Trading Spread in $'] = etfspread.unstack(level=1).loc[getmeHourDataFor]
        return ds


# Control function
# 1) Call runHistoricalArbitrageCalculations to get quotes and trade for a day
# 2) Call getMeHourdata to get data byh combining 2 dfs and returning one frame

if __name__ == "__main__":
    # Create an object of date when we need and time between which we need data
    previousdate = '2020-02-25'
    date = '2020-02-26'
    starttime = '9:30:00'
    endtime = '17:00:00'
    endtimeLoop = '16:00:00'
    etfticker = 'XLK'

    RunarbitrageObject = RunArbitrage(date=date, etfticker=etfticker)
    tradePricesDF, quotesSpreadDF = RunarbitrageObject.runHistoricalArbitrageCalculations()

    # for i in range(9, 16):
    #     print("Hour at=" + str(i))
    #     res = RunarbitrageObject.getMeHourdata(getmeHourDataFor=i, tradePricesDF=tradePricesDF,
    #                                            quotesSpreadDF=quotesSpreadDF)
    #     res['Arbitrage in $'] = abs(res['Arbitrage in $'])
    #     res['Flag'] = 0
    #     res.loc[(res['Arbitrage in $'] > res['ETF Trading Spread in $']) & res[
    #         'ETF Trading Spread in $'] != 0, 'Flag'] = 111
    #     print(res)
