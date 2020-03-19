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

    data = mongoengine.EmbeddedDocumentListField(TradesDataFields)

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
            dateWhenTradesWereFetched=datetime.datetime.now()
        )

        # Parse Trades Data Into Child EmbeddedDocument
        # This thing is taking too much time - KTZ In iterating over each row & saving
        # We can also save just as a Json rather than doing this
        print("Lot of time consumed in saving data as child data in object Line 60 StoreFetchQuotesData")
        for index, row in data.iterrows():
            tradesDataObj = TradesDataFields()
            tradesDataObj.TradePrice = row.p
            tradesDataObj.TradeSize = row.s
            tradesDataObj.TimeStamp = str(row.t)
            tradesDataObj.Exchange = str(row.x)

            tradesObj.data.append(tradesDataObj)
        print("Lot of time consumed in saving data as child data in object Line 69 StoreFetchQuotesData")

        # Saved Successfully
        try:
            tradesObj.save()
            return True
        except Exception as e:
            # failure in saving data
            print(e)
            return False

    def fetchDataFromTradesData(self, s=None, date=None):
        tradesD = TradesdataSchema.objects.filter(Q(symbol=s) & Q(dateForTrades=date)).first()
        tradesD = tradesD.to_json()
        return json.loads(tradesD)

    def doesItemExsistInTradesMongoDb(self, s=None, date=None):
        s = TradesdataSchema.objects.filter(Q(symbol=s) & Q(dateForTrades=date))
        # Return False if list is empty, that mean symbol, date combination doesn't exist and it needs to be downloaded
        return False if not s else True
