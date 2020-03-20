import mongoengine
mongoengine.connect('ETF_db', alias='ETF_db')


# {'Symbol' : symbol, dateForTrades : date, data : {'p' : Price, 's' : Size, 't' : Timestamp, 'x' : Exchange} }

##########
# Trades Data Base Schema
##########
class TradesdataSchema(mongoengine.Document):
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
        'collection': 'TradesData'
    }

