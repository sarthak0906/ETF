from pymongo import ASCENDING, DESCENDING
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.ETF_db

quotesCollection = db.QuotesData
quotesCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])

tradeCollection = db.TradesData
tradeCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])

dailyopencloseCollection=db.dailyopencloseCollection
dailyopencloseCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])