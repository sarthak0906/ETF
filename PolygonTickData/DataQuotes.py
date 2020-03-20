import sys
sys.path.append("..")  # Remove in production - KTZ


from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
from MongoDB.StoreFetchQuotesData import MongoQuotesData
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS


if __name__ == "__main__":
    ob = AssembleData(symbols=['XLK'], date='2020-03-13')
    
    dataExsist=MongoQuotesData().doesItemExsistInQuotesMongoDb
    createUrlsMethod=PolgonDataCreateURLS().PolygonHistoricQuotes
    saveDataMethod= MongoQuotesData().saveQuotesDataToMongo
    fetchDataMethod= MongoQuotesData().fetchDataFromQuotesData

    tradesDataDf = ob.getData(dataExsistMethod=dataExsist, 
        createUrlsMethod=createUrlsMethod, 
        saveDataMethod=saveDataMethod, 
        fetchDataMethod=fetchDataMethod)

    print(tradesDataDf)
