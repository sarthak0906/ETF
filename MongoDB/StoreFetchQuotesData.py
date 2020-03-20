import mongoengine
mongoengine.connect('ETF_db', alias='ETF_db')

from pymongo import MongoClient
client = MongoClient()
db = client.ETF_db

##########
# Quotes Data Base Schema 
########## 
class QuotesdataSchema(mongoengine.Document):
    symbol = mongoengine.StringField(required=True, max_length=200)
    dateForData = mongoengine.DateTimeField(required=True)
    dateWhenDataWasFetched = mongoengine.DateTimeField(required=True)
    batchSize = mongoengine.IntField(required=True)
    data = mongoengine.DynamicField()

    meta = {
    'indexes': [
            {
                'fields': ['symbol', 'dateForData','batchSize'],
                'unique': True
            }
        ],
        'db_alias': 'ETF_db',
        'collection': 'QuotesData'
    }
    

