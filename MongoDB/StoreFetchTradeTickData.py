import mongoengine
from mongoengine.queryset.visitor import Q
import datetime
import json

mongoengine.connect('ETF_db', alias='ETF_db')


# {'Symbol' : symbol, dateForTrades : date, data : {'p' : Price, 's' : Size, 't' : Timestamp, 'x' : Exchange} }
##########
# Trades Data Child Schema
##########
class TradesDataFields(mongoengine.EmbeddedDocument):
    TradePrice = mongoengine.FloatField()
    TradeSize = mongoengine.FloatField()
    TimeStamp = mongoengine.StringField()
    Exchange = mongoengine.StringField()


##########
# Trades Data Base Schema
##########
class TradesdataSchema(mongoengine.Document):
    symbol = mongoengine.StringField(required=True, max_length=200)
    dateForTrades = mongoengine.DateTimeField(required=True)
    dateWhenTradesWereFetched = mongoengine.DateTimeField(required=True)
    data = mongoengine.DynamicField()

    meta = {
        'indexes': [
            {
                'fields': ['symbol', 'dateForTrades'],
                'unique': True
            }
        ],
        'db_alias': 'ETF_db',
        'collection': 'TradesData'
    }


##########
# Save and Fetch Trades Data
##########
class MongoTradesData(object):

    def __init__(self):
        pass

    def saveTradesDataToMongo(self, symbol=None, dateForTrades=None, data=None):
        tradesObj = TradesdataSchema(
            symbol=symbol,
            dateForTrades=datetime.datetime.strptime(dateForTrades, '%Y-%m-%d'),
            dateWhenTradesWereFetched=datetime.datetime.now(),
            data=data.to_json(orient='records')
        )
        # Parse Trades Data Into Child EmbeddedDocument
        # This thing is taking too much time - KTZ In iterating over each row & saving
        # We can also save just as a Json rather than doing this

        try:
            tradesObj.save()
            return True
        except Exception as e:
            # failure in saving data
            print(e)
            return False

    def fetchDataFromTradesData(self, s=None, date=None):
        tradesD = TradesdataSchema.objects.filter(Q(symbol=s) & Q(dateForTrades=date)).first()
        tradesD = tradesD.to_mongo().to_dict()
        return tradesD

    def doesItemExsistInTradesMongoDb(self, s=None, date=None):
        s = TradesdataSchema.objects.filter(Q(symbol=s) & Q(dateForTrades=date))
        # Return False if list is empty, that mean symbol, date combination doesn't exist and it needs to be downloaded
        return False if not s else True
