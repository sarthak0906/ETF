##########
# Save and Fetch Quotes Data
##########
import sys
sys.path.append("..")  # Remove in production - KTZ
import datetime
import mongoengine
from mongoengine.queryset.visitor import Q
mongoengine.connect('ETF_db', alias='ETF_db')

from pymongo import MongoClient
client = MongoClient()
db = client.ETF_db

from MongoDB.StoreFetchQuotesData import QuotesdataSchema
from MongoDB.StoreFetchTradeTickData import TradesdataSchema

class MongoTradesQuotesData(object):

    def __init__(self):
        pass

    def saveDataInBatches(self, symbol=None, datetosave=None, savedata=None, batchSize=None, dataschematype=None):
        print(symbol + " BatchSize is=" + str(batchSize))

        dataObj = dataschematype(
            symbol=symbol,
            dateForData=datetime.datetime.strptime(datetosave, '%Y-%m-%d'),
            dateWhenDataWasFetched=datetime.datetime.now(),
            data=savedata,
            batchSize=batchSize
        )

        # Saved Successfully
        try:
            dataObj.save()
            return True
        except Exception as e:
            # failure in saving data
            print(e)
            return False

    def saveDataToMongo(self, symbol=None, datetosave=None, savedata=None, dataschematype=None):
        if not self.doesItemExsistInQuotesTradesMongoDb(s=symbol, date=datetosave, dataschematype=dataschematype):
            batchSize = 0
        else:
            # Object already exsists we need to increment Batch Size and add new Document For it. We retrieve last entry
            dataD = dataschematype.objects.filter(Q(symbol=symbol) & Q(dateForData=datetosave)).order_by(
                '-id').first()
            dataD = dataD.to_mongo().to_dict()
            batchSize = dataD['batchSize'] + 1

        return self.saveDataInBatches(symbol=symbol, datetosave=datetosave, savedata=savedata, batchSize=batchSize, dataschematype=dataschematype)

    def fetchQuotesTradesDataFromMongo(self, s=None, date=None, dataschematype=None):
        dataD = dataschematype.objects.filter(Q(symbol=s) & Q(dateForData=date)).first()
        dataD = dataD.to_mongo().to_dict()
        return dataD

    def doesItemExsistInQuotesTradesMongoDb(self, s=None, date=None, dataschematype=None):
        s = dataschematype.objects.filter(Q(symbol=s) & Q(dateForData=date))
        # Return False is list is empty, that mean symbol, date combination doesn't exsist and it needs to be downloaded
        return False if not s else True
