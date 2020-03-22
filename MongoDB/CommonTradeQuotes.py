##########
# Save and Fetch Quotes Data
##########
import sys
sys.path.append("..")  # Remove in production - KTZ

import datetime
import mongoengine
from mongoengine.queryset.visitor import Q
mongoengine.connect('ETF_db', alias='ETF_db')

class MongoTradesQuotesData(object):

    def __init__(self):
        pass

    def insertIntoCollection(self, symbol=None, datetosave=None, savedata=None, CollectionName=None, batchSize=None):
        print(symbol + " BatchSize is=" + str(batchSize))
        inserData={'symbol':symbol, 
                'dateForData':datetosave, 
                'dateWhenDataWasFetched': datetime.datetime.today().strftime('%Y-%m-%d'),
                'data':savedata,
                'batchSize':batchSize}
        CollectionName.insert_one(inserData)

    def fetchQuotesTradesDataFromMongo(self, s=None, date=None, CollectionName=None):
        combineddata = []
        dataD = CollectionName.find(symbol__in=s, dateForData=date)
        return [combineddata.extend(item.to_mongo().to_dict()['data']) for item in data]
        

    def doesItemExsistInQuotesTradesMongoDb(self, s=None, date=None, CollectionName=None):
        s= CollectionName.find({'symbol':s,'dateForData':date}).count()
        # Return False is list is empty, that mean symbol, date combination doesn't exsist and it needs to be downloaded
        return False if s==0 else True





        





