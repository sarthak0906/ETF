# API to get Trades Data
# Check if Trades data already exists in MongoDB, If Does fetch from MongoDb
# If Doesn't exist fetch from polygon and save in MongoDb

# Gather trades data in AssembleTradesData and return 'READY' a Trades pandas dataframe object
import sys

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
import datetime

from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from PolygonTickData.FetchPolygonDataForUrls import FetchPolygonData
from MongoDB.StoreFetchTradeTickData import MongoTradesData
from PolygonTickData.Helper import Helper


class PolygonTradesData(object):

    def fetchTradesDataFromPolygonAPI(self, tradesRoutines=None, date=None):
        objFetchData = FetchPolygonData(date=date, PolygonMethod=PolgonDataCreateURLS().PolygonHistoricTrades)
        finalResultDict = objFetchData.getDataFromPolygon(getUrls=tradesRoutines, finalResultDict=[])
        return pd.DataFrame(finalResultDict)[['Symbol', 'p', 's', 't', 'x']]

    def saveTradesDataInMongoDB(self, symbol=None, dateForTrades=None, data=None):
        objMongoTrades = MongoTradesData()
        savingStatus = objMongoTrades.saveTradesDataToMongo(symbol=symbol, dateForTrades=dateForTrades, data=data)
        if savingStatus:
            print("Saved Succesfully {} for {} at {}".format(symbol, dateForTrades, datetime.datetime.now()))
        else:
            print("Error Occured While Saving {} for {} at {}".format(symbol, dateForTrades, datetime.datetime.now()))

    # Check if symbol,date pair exist in MongoDB, If don't exist download URLs for the symbols
    def checkIfTradesDataExsistInMongoDB(self, symbols=None, date=None):
        objMongoTrades = MongoTradesData()
        symbolsToBeDownloaded = []
        for symbol in symbols:
            if not objMongoTrades.doesItemExsistInTradesMongoDb(symbol, date):
                symbolsToBeDownloaded.append(symbol)
        return symbolsToBeDownloaded

    def fetchTradesDataFromMongoDB(self, symbols=None, date=None):
        objMongoTrades = MongoTradesData()
        data = []
        for symbol in symbols:
            tradesDictData = objMongoTrades.fetchDataFromTradesData(s=symbol, date=date)
            data = data + (tradesDictData['data'])
        return pd.DataFrame(data)

    def createTradesUrlsForStocks(self, symbols=None, date=None, endTs=None):
        createUrls = PolgonDataCreateURLS()
        tradesRoutines = [createUrls.PolygonHistoricTrades(date=date, symbol=symbol, startTS=None, endTS=endTs,
                                                           limitresult=str(50000)) for symbol in symbols]
        return tradesRoutines


class AssembleTradesData(object):
    def __init__(self, symbols=None, date=None):
        self.date = date
        self.endTs = Helper().convertHumanTimeToUnixTimeStamp(date=self.date, time='17:00:00')
        self.symbols = symbols
        self.objTrades = PolygonTradesData()

    def getTradesData(self):
        # Perform check if symbols need to be downloaded or they already exist in the DB
        symbolsToBeDownloaded = self.objTrades.checkIfTradesDataExsistInMongoDB(symbols=self.symbols, date=self.date)
        # Check if any symbol needs to be downloaded
        if symbolsToBeDownloaded:
            # Create URLs
            tradesRoutines = self.objTrades.createTradesUrlsForStocks(symbols=symbolsToBeDownloaded, date=self.date,
                                                                      endTs=self.endTs)
            # Fetch Data for URLs
            finalResultDf = self.objTrades.fetchTradesDataFromPolygonAPI(tradesRoutines=tradesRoutines, date=self.date)

            print("DataTrades.py Time to Do a query over symbol in Pandas Dataframe Line 73")
            # Save the finalResultDf into MongoDb one by one for each symbol
            # This thing is taking too much time - KTZ In searching over symbol
            for symbol in symbolsToBeDownloaded:
                data = finalResultDf[finalResultDf['Symbol'] == symbol]
                _ = self.objTrades.saveTradesDataInMongoDB(symbol=symbol, dateForTrades=self.date, data=data)
            print("DataTrade.py - Line 79 ")

        # Prepare to Return a dataframe for the Symbols
        return self.objTrades.fetchTradesDataFromMongoDB(symbols=self.symbols, date=self.date)


if __name__ == "__main__":
    ob = AssembleTradesData(symbols=['XLK', 'AAPL', 'MSFT'], date='2020-03-13')
    tradesDataDf = ob.getTradesData()
    print(tradesDataDf)
