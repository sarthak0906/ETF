from pymongo import ASCENDING, DESCENDING
from pymongo import MongoClient
import motor.motor_asyncio
import asyncio

#connectionLocal = MongoClient('localhost', 27017)
connectionLocal = MongoClient('18.213.229.80', 27017)
db = connectionLocal.ETF_db

#motor_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
motor_client = motor.motor_asyncio.AsyncIOMotorClient('18.213.229.80', 27017)
motor_db = motor_client.ETF_db

# Quotes Pipeline
quotesCollection = db.QuotesData
quotesCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])
quotespipeline = [
    {'$match': ''},
    {'$unwind': '$data'},
    {'$group': {
        '_id': '$_id',
        'data': {'$push': {
            'Symbol': '$data.Symbol',
            'Time': '$data.t',
            'Bid Price': '$data.p',
            'Bid Size': '$data.s',
            'Ask Price': '$data.P',
            'Ask Size': '$data.S',
        }}
    }}
]

# Trades Pipeline
tradeCollection = db.TradesData
tradeCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])
tradespipeline = [
    {'$match': ''},
    {'$unwind': '$data'},
    {'$group': {
        '_id': '$_id',
        'data': {'$push': {
            'Symbol': '$data.Symbol',
            'Time': '$data.t',
            'High Price': '$data.h',
            'Low Price': '$data.l',
            'Trade Size': '$data.v',
            'Number of Trades': '$data.n',
        }}
    }}
]

# Daily Open Close Collection
dailyopencloseCollection = db.DailyOpenCloseCollection
dailyopencloseCollection.create_index([("dateForData", DESCENDING), ("Symbol", ASCENDING)], unique=True)

# Arbitrage
arbitragecollection = db.ArbitrageCollection
arbitragecollection.create_index([("dateOfAnalysis", DESCENDING), ("ETFName", ASCENDING)], unique=True)

# Arbitrage Per Minute
arbitrage_per_min = db.ArbitragePerMin
arbitrage_per_min.create_index([('Timestamp', DESCENDING)])

# Trade Aggregate Minute for all Tickers.
# Cursor for pulling data (PyMongo Cursor)
trade_per_min_WS = db.TradePerMinWS
# Cursor for insert action into TradePerMinWS (AsyncIOMotorCursor)
trade_per_min_WS_motor = motor_db.TradePerMinWS

quotesWS_collection = db.QuotesLiveData

connectionLocal.close()
