import sys

sys.path.append("..")  # Remove in production - KTZ

from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
from MongoDB.StoreFetchTradeTickData import TradesdataSchema
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from MongoDB.CommonTradeQuotes import MongoTradesQuotesData

if __name__ == "__main__":
    ob = AssembleData(symbols=['XLK', 'AAPL', 'MSFT'], date='2020-03-13')

    dataExsist = MongoTradesQuotesData().doesItemExsistInQuotesTradesMongoDb
    createUrlsMethod = PolgonDataCreateURLS().PolygonHistoricTrades
    saveDataMethod = MongoTradesQuotesData().saveDataToMongo
    fetchDataMethod = MongoTradesQuotesData().fetchQuotesTradesDataFromMongo
    dataschematype = TradesdataSchema
    tradesDataDf = ob.getData(dataExsistMethod=dataExsist,
                              createUrlsMethod=createUrlsMethod,
                              saveDataMethod=saveDataMethod,
                              fetchDataMethod=fetchDataMethod,
                              dataschematype=dataschematype)

    print(tradesDataDf)
