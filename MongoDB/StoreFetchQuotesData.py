import mongoengine
from mongoengine.queryset.visitor import Q
import datetime
import json
import sys
mongoengine.connect('ETF_db', alias='ETF_db')

from pymongo import MongoClient
client = MongoClient()
db = client.ETF_db

##########
# Quotes Data Base Schema 
########## 
class QuotesdataSchema(mongoengine.Document):
    symbol = mongoengine.StringField(required=True, max_length=200)
    dateForQuotes = mongoengine.DateTimeField(required=True)
    dataWhenQuotesWereFetched = mongoengine.DateTimeField(required=True)
    batchSize = mongoengine.IntField(required=True)
    data = mongoengine.DynamicField()

    meta = {
    'indexes': [
            {
                'fields': ['symbol', 'dateForQuotes','batchSize'],
                'unique': True
            }
        ],
        'db_alias': 'ETF_db',
        'collection': 'QuotesData'
    }
    

##########
# Save and Fetch Quotes Data
########## 
class MongoQuotesData(object):

    def __init__(self):
        pass

    def saveQuotesInBatches(self,symbol=None, datetosave=None, savedata=None, batchSize=None):
        print("batchSize is="+str(batchSize))
        quotesObj = QuotesdataSchema(
            symbol=symbol,
            dateForQuotes=datetime.datetime.strptime(datetosave, '%Y-%m-%d'),
            dataWhenQuotesWereFetched=datetime.datetime.now(),
            data=savedata,
            batchSize=batchSize
        )
        # Saved Successfully
        try:
            quotesObj.save()
            return True
        except Exception as e:
            # failure in saving data
            print(e)
            return False

    def saveQuotesDataToMongo(self, symbol=None, datetosave=None, savedata=None):
        if not self.doesItemExsistInQuotesMongoDb(s=symbol, date=datetosave):
            print("First time")
            batchSize=0
        else:
            print("second time")
            # Object already exsists we need to increment Batch Size and add new Document For it. We retrieve last entry
            quotesD = QuotesdataSchema.objects.filter(Q(symbol=symbol) & Q(dateForQuotes=datetosave)).order_by('-id').first()
            quotesD = quotesD.to_mongo().to_dict()
            batchSize=quotesD['batchSize']+1
    
        return self.saveQuotesInBatches(symbol=symbol, datetosave=datetosave, savedata=savedata, batchSize=batchSize)

    def fetchDataFromQuotesData(self, s=None, date=None):
        quotesD = QuotesdataSchema.objects.filter(Q(symbol=s) & Q(dateForQuotes=date)).first()
        quotesD = quotesD.to_mongo().to_dict()
        return quotesD

    def doesItemExsistInQuotesMongoDb(self, s=None, date=None):
        s = QuotesdataSchema.objects.filter(Q(symbol=s) & Q(dateForQuotes=date))
        # Return False is list is empty, that mean symbol, date combination doesn't exsist and it needs to be downloaded
        return False if not s else True
