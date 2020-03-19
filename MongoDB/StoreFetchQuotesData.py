import mongoengine
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
		
		# Saved Successfully
		try:
			quotesObj.save()
			return True
		except Exception as e:
			# failure in saving data
			print(e)
			return False

	def doesItemExsistInQuotesMongoDb(self, s=None, date=None):
		s = QuotesdataSchema.objects(symbol='XLP',dateForQuotes='ISODate({})'.format(date))
		return True if len(s)==1 else False
		









