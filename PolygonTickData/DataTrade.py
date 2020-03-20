import sys
sys.path.append("..")  # Remove in production - KTZ


from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
from MongoDB.StoreFetchTradeTickData import MongoTradesData
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS


if __name__ == "__main__":
    ob = AssembleData(symbols=['XLK', 'AAPL', 'MSFT'], date='2020-03-13')
    
    dataExsist=MongoTradesData().doesItemExsistInTradesMongoDb
    createUrlsMethod=PolgonDataCreateURLS().PolygonHistoricTrades
    saveDataMethod= MongoTradesData().saveTradesDataToMongo
    fetchDataMethod= MongoTradesData().fetchDataFromTradesData

    tradesDataDf = ob.getData(dataExsistMethod=dataExsist, 
        createUrlsMethod=createUrlsMethod, 
        saveDataMethod=saveDataMethod, 
        fetchDataMethod=fetchDataMethod)

    print(tradesDataDf)
