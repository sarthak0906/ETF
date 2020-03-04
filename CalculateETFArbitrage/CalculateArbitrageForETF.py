#####
# Remove in production - KTZ
#####
import sys

sys.path.append("..")
#####
# Remove in production - KTZ
#####

import requests
from datetime import datetime
import requests
import json
import time
import pandas as pd
from time import mktime
import asyncio

from PolygonTickData.PolygonDataAPIConnection import *
from CalculateETFArbitrage.helper import Helper


class LoadWeightsFromMongoDB(object):

    def __init__(self):
        pass
        self.etfname = 'XLK'
        self.date = '0200226'

    def getWeightsFromMongoDB(self, ticker=None, date=None):
        # Taking in ETF List -
        # holdings = pd.read_csv("XLK-holdings20200226.csv")
        holdings = Helper().getHoldingsDatafromDB('XLK', '20200226')

        # Clean the Data as Needed
        # holdings['TickerWeight'] = holdings['TickerWeight'].apply(lambda x: x.replace('%', ''))
        # holdings['TickerWeight'] = holdings['TickerWeight'].astype(float)
        holdings['TickerWeight'] = holdings['TickerWeight'] / 100
        weights = dict(zip(holdings.TickerSymbol, holdings.TickerWeight))
        cashvalue = holdings[holdings['TickerSymbol'] == 'CASH'].get('TickerWeight').item() * 28583351000
        symbols = list(holdings['TickerSymbol'].values) + ['XLK']
        symbols.remove('CASH')

        etfholdingsdata = {'weights': weights, 'symbols': symbols, 'cashvalue': cashvalue}
        return etfholdingsdata


# Main class used for running
class RunArbitrage(object):

    def __init__(self, date=None, previousdate=None, starttime='9:30:00', endtime='17:00:00', endtimeLoop='16:00:00',
                 etfticker=None):
        self.date = date
        self.starttime = starttime
        self.endtime = endtime
        self.endtimeLoop = endtimeLoop
        self.extractDataTillTime = Helper().stringTimeToDatetime(date=self.date, time=self.endtimeLoop)
        self.marketTimeStamps = Helper().convertStringDateToTS(date=self.date, starttime=self.starttime,
                                                               endtime=self.endtime)
        self.etfticker = etfticker
        self.etfholdingsdata = []

    # Fetches data from Polygon using conditions if data is achieved till 5 pm or not
    # Called 2nd from runHistoricalArbitrageCalculations
    async def getDataFromPolygon(self, symbol, methodPassed):
        tickHistData = {}
        # First Request
        data = methodPassed(date=self.date, symbol=symbol, endTS=self.marketTimeStamps['marketCloseTS'],
                            limitresult=str(50000))
        # Last timestamp from data received
        lastUnixTimeStamp = data['results'][-1]['t']
        # Covert UNIX timestamp to human timestamp
        lastHumanTimeStamp = Helper().getHumanTime(lastUnixTimeStamp)
        # Get timestamp for date +  '18:00:00' hrs - Make use of pagination
        # Paginated Request if the data from above doesn't reach 5 pm time
        await asyncio.sleep(0.2)
        while lastHumanTimeStamp < self.extractDataTillTime:
            print(Helper().getHumanTime(data['results'][-1]['t']))
            data2 = methodPassed(date=self.date, symbol=symbol, startTS=str(lastUnixTimeStamp),
                                 endTS=self.marketTimeStamps['marketCloseTS'], limitresult=str(50000))
            # Last timestamp from data received
            lastUnixTimeStamp = data2['results'][-1]['t']
            # Covert UNIX timestamp to human timestamp
            lastHumanTimeStamp = Helper().getHumanTime(lastUnixTimeStamp)
            # Get timestamp for date +  '18:00:00' hrs - Make use of pagination
            data['results'] = data['results'] + data2['results']
            await asyncio.sleep(0.2)
        tickHistData[symbol] = data
        # print(tickHistData)
        return tickHistData

    # call this to run the data extractor
    # Calles First
    def runHistoricalArbitrageCalculations(self):
        # Get Weights Holdings
        self.etfholdingsdata = LoadWeightsFromMongoDB().getWeightsFromMongoDB()

        tickHistDataQuotes = {}
        tickHistDataTrade = {}
        priceforNAVfilling = {}

        Polygonobj = PolgonData()

        # shorted symbols for testing - remove for production
        # self.etfholdingsdata['symbols']=['TXN','V','XLK']

        #########**************#########
        # I guess threading will come here, because here we want to thead getting of 1 complete ticker data
        # So 1 thread for AAPL will complete tickHistDataQuotes,tickHistDataTrade,priceforNAVfilling
        # So you can have 10 threads for a ticker each. And each thread will complete the get
        # Challenge will be to store same threads data in same tickHistDataQuotes,tickHistDataTrade, they are sharing resources
        # Feel free to move below for loop in a seperate method
        #########**************#########


        # for symbol in self.etfholdingsdata['symbols']:
        #     tickHistDataQuotes[symbol] = self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricQuotes)
        #     tickHistDataTrade[symbol] = self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricTrades)
        #
        #     # For NA values for a day, fill it with NA values
        #     dfTemp = Polygonobj.PolygonDailyOpenClose(date=date, symbol=symbol)
        #     priceforNAVfilling[symbol] = dfTemp['open']


        #########**************#########
        # I guess threading will come here, because here we want to thead getting of 1 complete ticker data
        # So 1 thread for AAPL will complete tickHistDataQuotes,tickHistDataTrade,priceforNAVfilling
        # So you can have 10 threads for a ticker each. And each thread will complete the get
        # Challenge will be to store same threads data in same tickHistDataQuotes,tickHistDataTrade, they are sharing resources
        # Feel free to move below for loop in a seperate method
        #########**************#########

###################### ASYNCIO OVER HERE #####################################
        async def main_():
            async def one_iter(semaphore_, symbol):
                async with semaphore_:
                    #print(self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricQuotes))
                    tickHistDataQuotes[symbol] = await self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricQuotes)
                    tickHistDataTrade[symbol] = await self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricTrades)
                    dfTemp = Polygonobj.PolygonDailyOpenClose(date=date, symbol=symbol)
                    priceforNAVfilling[symbol] = dfTemp['open']
            semaphore = asyncio.BoundedSemaphore(3)
            co_routines = [one_iter(semaphore, symbol) for symbol in self.etfholdingsdata['symbols']]
            # co_routines = [one_iter(semaphore, symbol) for symbol in ['AAPL','MSFT','XLK']]
            await asyncio.gather(*co_routines)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main_())
##################### ASYNCIO COMPLETES HERE #################################
        # print(tickHistDataTrade)

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
        # del tickHistDataTrade
        # del tickHistDataQuotes

        #########**************#########
        # Needs Threading in time conversion #
        #########**************#########
        tradeData['t'] = tradeData['t'].apply(lambda x: helperObj.getHumanTime(x, getMilliSecondsAlso=False))
        quotesData['t'] = quotesData['t'].apply(lambda x: helperObj.getHumanTime(x, getMilliSecondsAlso=False))

        quotesData['Spread'] = quotesData['P'] - quotesData['p']
        quotesData['MidPrice'] = (quotesData['P'] + quotesData['p']) / 2

        # Group Trade Data by minutes
        tradePrices = tradeData.groupby([tradeData['t'].dt.hour, tradeData['t'].dt.minute, tradeData['Symbol']])[
            'p'].mean()
        tradePricesDF = tradePrices.unstack(level=2)
        tradePricesDF = tradePricesDF.fillna(method='ffill')
        tradePricesDF = tradePricesDF.fillna(priceforNAVfilling)

        # Group Quotes Data by minutes
        quotesSpreads = quotesData.groupby([quotesData['t'].dt.hour, quotesData['t'].dt.minute, quotesData['Symbol']])[
            'Spread'].mean()
        quotesSpreadDF = quotesSpreads.unstack(level=2)
        quotesSpreadDF = quotesSpreadDF.fillna(0)

        return tradePricesDF, quotesSpreadDF

    # Once we have tradePrices and quotesSpread we can call this which will give data for hour for that day
    # Called once we have tradePricesDF,quotesSpreadDF independently
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

    RunarbitrageObject = RunArbitrage(date=date, previousdate=previousdate, starttime='9:30:00', endtime='17:00:00',
                                      endtimeLoop='16:00:00', etfticker=etfticker)
    tradePricesDF, quotesSpreadDF = RunarbitrageObject.runHistoricalArbitrageCalculations()

    for i in range(9, 16):
        print("Hour at=" + str(i))
        res = RunarbitrageObject.getMeHourdata(getmeHourDataFor=i, tradePricesDF=tradePricesDF,
                                               quotesSpreadDF=quotesSpreadDF)
        res['Arbitrage in $'] = abs(res['Arbitrage in $'])
        res['Flag'] = 0
        res.loc[(res['Arbitrage in $'] > res['ETF Trading Spread in $']) & res[
            'ETF Trading Spread in $'] != 0, 'Flag'] = 111
        print(res)
