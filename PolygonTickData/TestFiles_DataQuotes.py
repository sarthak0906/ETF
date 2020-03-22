import sys

sys.path.append("..")  # Remove in production - KTZ

from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
from MongoDB.Schemas import QuotesdataSchema
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from MongoDB.CommonTradeQuotes import MongoTradesQuotesData

if __name__ == "__main__":
    ob = AssembleData(symbols=['XLK'], date='2020-03-16')

    dataExsist = MongoTradesQuotesData().doesItemExsistInQuotesTradesMongoDb
    createUrlsMethod = PolgonDataCreateURLS().PolygonHistoricQuotes
    saveDataMethod = MongoTradesQuotesData().saveDataToMongo
    fetchDataMethod = MongoTradesQuotesData().fetchQuotesTradesDataFromMongo
    dataschematype = QuotesdataSchema
    quotesDataDf = ob.getData(dataExsistMethod=dataExsist,
                              createUrlsMethod=createUrlsMethod,
                              saveDataMethod=saveDataMethod,
                              fetchDataMethod=fetchDataMethod,
                              dataschematype=quotesCollection)
    print(quotesDataDf)
