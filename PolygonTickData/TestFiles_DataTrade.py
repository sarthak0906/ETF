import sys

sys.path.append("..")  # Remove in production - KTZ

from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
from MongoDB.Schemas import tradeCollection
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from MongoDB.CommonTradeQuotes import MongoTradesQuotesData
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata

if __name__ == "__main__":
    etfData=LoadHoldingsdata(etfname='XLK', fundholdingsdate='2020-03-16')
    ob = AssembleData(symbols=etfData.getSymbols(), date='2020-03-16')

    tradesDataDf = ob.getData(dataExsistMethod=MongoTradesQuotesData().doesItemExsistInQuotesTradesMongoDb,
                              createUrlsMethod=PolgonDataCreateURLS().PolygonHistoricTrades,
                              insertIntoCollection=MongoTradesQuotesData().insertIntoCollection,
                              fetchDataMethod= MongoTradesQuotesData().fetchQuotesTradesDataFromMongo,
                              CollectionName=tradeCollection)
    print(tradesDataDf)
