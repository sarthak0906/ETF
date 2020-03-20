# API to get Trades Data
# Check if Trades data already exists in MongoDB, If Does fetch from MongoDb
# If Doesn't exist fetch from polygon and save in MongoDb

# Gather trades data in AssembleTradesData and return 'READY' a Trades pandas dataframe object
import sys

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
import datetime
import ast 

from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from PolygonTickData.FetchPolygonDataForUrls import FetchPolygonData
from MongoDB.StoreFetchTradeTickData import MongoTradesData
from PolygonTickData.Helper import Helper


class PolygonTradesData(object):

    def fetchTradesDataFromPolygonAPI(self, tradesRoutines=None, date=None, storeDataInMongo=None):
        objFetchData = FetchPolygonData(date=date, PolygonMethod=PolgonDataCreateURLS().PolygonHistoricTrades, storeDataInMongo=storeDataInMongo)
        storageAndCrawlingStatus = objFetchData.getDataFromPolygon(getUrls=tradesRoutines)
        if storageAndCrawlingStatus:
            print("Data was successfully got and stored")
        else:
            print("Issue occured while getting & saving data from Polygon")
    
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
        dictlist = []
        dictlistfinal = []
        for symbol in symbols:
            tradesDictData = objMongoTrades.fetchDataFromTradesData(s=symbol, date=date)
            data = data + tradesDictData['data']
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
            _ = self.objTrades.fetchTradesDataFromPolygonAPI(tradesRoutines=tradesRoutines, date=self.date, storeDataInMongo= MongoTradesData().saveTradesDataToMongo)

        # Prepare to Return a dataframe for the Symbols
        return self.objTrades.fetchTradesDataFromMongoDB(symbols=self.symbols, date=self.date)


if __name__ == "__main__":
    ob = AssembleTradesData(symbols=['XLK', 'AAPL', 'MSFT'], date='2020-03-13')
    tradesDataDf = ob.getTradesData()
    print(tradesDataDf)
