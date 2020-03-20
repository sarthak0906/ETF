import sys

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
import datetime

from PolygonTickData.FetchPolygonDataForUrls import FetchPolygonData
from PolygonTickData.Helper import Helper
from MongoDB.CommonTradeQuotes import MongoTradesQuotesData


class PolygonQuotesTradesData(object):
    def __init__(self):
        self.mtqd = MongoTradesQuotesData()

    # Fetch Data from Polygon API
    def fetchDataFromPolygonAPI(self, Routines=None, date=None, storeDataInMongo=None, PolygonMethodForUrls=None,
                                dataschematype=None):
        objFetchData = FetchPolygonData(date=date, PolygonMethod=PolygonMethodForUrls,
                                        storeDataInMongo=storeDataInMongo, dataschematype=dataschematype)
        storageAndCrawlingStatus = objFetchData.getDataFromPolygon(getUrls=Routines)
        if storageAndCrawlingStatus:
            print("Data was successfully got and stored")
        else:
            print("Issue occured while getting & saving data from Polygon")

    # Check if symbol,date pair exist in MongoDB, If don't exist download URLs for the symbols
    def checkIfDataExsistInMongoDB(self, symbols=None, date=None, dataschematype=None):
        symbolsToBeDownloaded = []
        for symbol in symbols:
            if not self.mtqd.doesItemExsistInQuotesTradesMongoDb(symbol, date, dataschematype):
                symbolsToBeDownloaded.append(symbol)
        return symbolsToBeDownloaded

    # Fetch Data from MongoDb
    def fetchDataFromMongoDB(self, symbols=None, date=None, dataschematype=None):
        data=[] # Will become a list of all dictionary elements
        for symbol in symbols:
            DictData = self.mtqd.fetchQuotesTradesDataFromMongo(s=symbol, date=date,
                                                                            dataschematype=dataschematype)
            DictData = [dict(item, **{'Symbol': symbol}) for item in DictData]
            # DictData returns a list of dictionary elements
            data.extend(DictData)
        return pd.DataFrame(data)

    # Create Urls to get data for
    def createUrlsForStocks(self, symbols=None, date=None, endTs=None, PolygonMethodForUrls=None):
        Routines = [PolygonMethodForUrls(date=date, symbol=symbol, startTS=None, endTS=endTs, limitresult=str(50000))
                    for symbol in symbols]
        return Routines


class AssembleData(object):
    def __init__(self, symbols=None, date=None):
        self.date = date
        self.endTs = Helper().convertHumanTimeToUnixTimeStamp(date=self.date, time='17:00:00')
        self.symbols = symbols
        self.obj = PolygonQuotesTradesData()

    def getData(self, dataExsistMethod=None, createUrlsMethod=None, saveDataMethod=None, fetchDataMethod=None,
                dataschematype=None):
        # Perform check if symbols need to be downloaded or they already exist in the DB
        symbolsToBeDownloaded = self.obj.checkIfDataExsistInMongoDB(symbols=self.symbols, date=self.date,
                                                                    dataschematype=dataschematype)
        # Check if any symbol needs to be downloaded
        if symbolsToBeDownloaded:
            # Create URLs
            Routines = self.obj.createUrlsForStocks(symbols=symbolsToBeDownloaded, date=self.date,
                                                    endTs=self.endTs,
                                                    PolygonMethodForUrls=createUrlsMethod)
            # Fetch Data for URLs
            _ = self.obj.fetchDataFromPolygonAPI(Routines=Routines, date=self.date,
                                                 storeDataInMongo=saveDataMethod,
                                                 PolygonMethodForUrls=createUrlsMethod, dataschematype=dataschematype)

        # Prepare to Return a dataframe for the Symbols
        resultdf = self.obj.fetchDataFromMongoDB(symbols=self.symbols, date=self.date,
                                                 dataschematype=dataschematype)

        return resultdf
