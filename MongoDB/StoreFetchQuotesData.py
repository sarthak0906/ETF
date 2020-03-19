import mongoengine
from mongoengine.queryset.visitor import Q
import datetime
import json
mongoengine.connect('ETF_db', alias='ETF_db')


########## 
# Quotes Data Child Schema 
########## 
class QuotesDataFields(mongoengine.EmbeddedDocument):
	# {'Symbol': 'XLK', 'P': 80.24, 'S': 2, 'p': 80.21, 's': 3, 't': 1584106568115843860, 'X': 12, 'x': 8}
    AskPrice = mongoengine.FloatField()
    AskSize = mongoengine.FloatField()
    BidPrice = mongoengine.FloatField()
    BidSize = mongoengine.FloatField()
    AskExchange =mongoengine.StringField()
    BidExchange =mongoengine.StringField()
    TimeStamp = mongoengine.StringField()

########## 
# Quotes Data Base Schema 
########## 
class QuotesdataSchema(mongoengine.Document):
    symbol = mongoengine.StringField(required=True, max_length=200)
    dateForQuotes = mongoengine.DateTimeField(required=True)
    dataWhenQuotesWereFetched = mongoengine.DateTimeField(required=True)
    
    data = mongoengine.EmbeddedDocumentListField(QuotesDataFields)

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
			dataWhenQuotesWereFetched=datetime.datetime.now()
			)

		# Parse Quotes Data Into Child EmbeddedDocument
		# This thing is taking too much time - KTZ In iterating over each row & saving
		# We can also save just as a Json rather than doing this
		print("Lot of time consumed in saving data as child data in object Lin3 59 StoreFetchQuotesData")
		for index, row in data.iterrows():
			quotesDataObj = QuotesDataFields()
			quotesDataObj.AskPrice=row.P
			quotesDataObj.AskSize=row.S
			quotesDataObj.BidPrice=row.p
			quotesDataObj.BidSize=row.s
			quotesDataObj.AskExchange=str(row.X)
			quotesDataObj.BidExchange=str(row.x)
			quotesDataObj.TimeStamp=str(row.t)

			quotesObj.data.append(quotesDataObj)
		print("Lot of time consumed in saving data as child data in object Lin3 59 StoreFetchQuotesData")

		# Saved Successfully
		try:
			quotesObj.save()
			return True
		except Exception as e:
			# failure in saving data
			print(e)
			return False

	def fetchDataFromQuotesData(self,s=None, date=None):
		quotesD = QuotesdataSchema.objects.filter(Q(symbol=s) & Q(dateForQuotes=date)).first()
		quotesD=quotesD.to_json()
		return json.loads(quotesD)
		

	def doesItemExsistInQuotesMongoDb(self, s=None, date=None):
		s = QuotesdataSchema.objects.filter(Q(symbol=s) & Q(dateForQuotes=date))
		# Return False is list is empty, that mean symbol, date combination doesn't exsist and it needs to be downloaded
		return False if not s else True
		









