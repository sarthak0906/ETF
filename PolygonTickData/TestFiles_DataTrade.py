import sys

sys.path.append("..")  # Remove in production - KTZ

from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
from MongoDB.Schemas import tradeCollection
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from MongoDB.CommonTradeQuotes import MongoTradesQuotesData

if __name__ == "__main__":
    ob = AssembleData(symbols=['XLK', 'AAPL', 'MSFT'], date='2020-03-16')

    tradesDataDf = ob.getData(dataExsistMethod=MongoTradesQuotesData().doesItemExsistInQuotesTradesMongoDb,
                              createUrlsMethod=PolgonDataCreateURLS().PolygonHistoricTrades,
                              insertIntoCollection=MongoTradesQuotesData().insertIntoCollection,
                              fetchDataMethod= MongoTradesQuotesData().fetchQuotesTradesDataFromMongo,
                              CollectionName=tradeCollection)
    print(tradesDataDf)
