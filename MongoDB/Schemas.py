from pymongo import ASCENDING, DESCENDING
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.ETF_db

quotesCollection = db.QuotesData
quotesCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])

tradeCollection = db.TradesData
tradeCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])


