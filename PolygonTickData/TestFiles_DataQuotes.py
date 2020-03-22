import sys

sys.path.append("..")  # Remove in production - KTZ


from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
from MongoDB.Schemas import quotesCollection
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from CommonTradeQuotes.MongoTradesQuotesData import MongoTradesQuotesData

if __name__ == "__main__":
    ob = AssembleData(symbols=['XLK'], date='2020-03-16')
    quotesDataDf = ob.getData(dataExsistMethod=MongoTradesQuotesData().doesItemExsistInQuotesTradesMongoDb,
                              createUrlsMethod=PolgonDataCreateURLS().PolygonHistoricQuotes,
                              insertIntoCollection=MongoTradesQuotesData().saveDataToMongo,
                              fetchDataMethod=MongoTradesQuotesData().fetchQuotesTradesDataFromMongo,
                              CollectionName=quotesCollection)
    print(quotesDataDf)
