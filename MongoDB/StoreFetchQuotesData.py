import mongoengine
import datetime
import json
mongoengine.connect('ETF_db', alias='ETF_db')

########## 
# Quotes Data Schema
########## 
class QuotesdataSchema(mongoengine.Document):
    symbol = mongoengine.StringField(required=True, max_length=200)
    dateForQuotes = mongoengine.DateTimeField(required=True)
    dataWhenQuotesWereFetched = mongoengine.DateTimeField(required=True)
    data = mongoengine.DictField(required=True)

    meta = {
       'indexes': [
        {
            'fields': ['symbol', 'dateForQuotes'],
            'unique': True
        }
    ],
    'db_alias': 'ETF_db',
    'collection': 'QuotesData'
    }

class QuotesDaTaFields(mongoengine.EmbeddedDocument):
    'Ask Price' = mongoengine.StringField()
    TickerSymbol = mongoengine.StringField()
    TickerWeight = mongoengine.FloatField()


########## 
# Save and Fetch Quotes Data
########## 
class MongoQuotesData(object):

	def __init__(self):
		pass

	def saveQuotesDataToMongo(self, symbol=None, dateForQuotes=None, data=None):
		quotesObj = QuotesdataSchema(
			symbol=symbol,
			dateForQuotes=datetime.datetime.strptime(dateForQuotes,'%Y-%m-%d') ,
			dataWhenQuotesWereFetched=datetime.datetime.now(),
			data=data.to_dict('records')
			)
		# Saved Successfully
		try:
			quotesObj.save()
			return True
		except Exception as e:
			# failure in saving data
			print(e)
			return False


