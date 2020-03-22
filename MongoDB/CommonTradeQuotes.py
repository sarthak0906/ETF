##########
# Save and Fetch Quotes Data
##########
import sys
sys.path.append("..")  # Remove in production - KTZ

import datetime
import mongoengine
from mongoengine.queryset.visitor import Q
import json
from bson import json_util
mongoengine.connect('ETF_db', alias='ETF_db')

class MongoTradesQuotesData(object):

    def __init__(self,CollectionName=None, date=None):
        self.CollectionName=CollectionName
        self.date=date
    
    def insertIntoCollection(self, symbol=None, datetosave=None, savedata=None, CollectionName=None, batchSize=None):
        print(symbol + " BatchSize is=" + str(batchSize))
        inserData={'symbol':symbol, 
                'dateForData':datetime.datetime.strptime(datetosave,'%Y-%m-%d'), 
                'dateWhenDataWasFetched': datetime.datetime.today(),
                'data':savedata,
                'batchSize':batchSize}
        CollectionName.insert_one(inserData)

    def fetchQuotesTradesDataFromMongo(self, symbolList=None, date=None, CollectionName=None):
        query={'dateForData':datetime.datetime.strptime(date,'%Y-%m-%d'), 'symbol': { '$in': symbolList }}
        #explain=(CollectionName.find(query).explain())
        #print(json.dumps(explain, indent=2,default=json_util.default))
        # Cursor
        dataD = CollectionName.find(query)
        combineddata=[]
        [combineddata.extend(item['data']) for item in dataD]
        return combineddata
    
    def doesItemExsistInQuotesTradesMongoDb(self, s=None, date=None, CollectionName=None):
        s= CollectionName.find({'symbol':s,'dateForData':datetime.datetime.strptime(date,'%Y-%m-%d')}).count()
        # Return False is list is empty, that mean symbol, date combination doesn't exsist and it needs to be downloaded
        return False if s==0 else True





        





