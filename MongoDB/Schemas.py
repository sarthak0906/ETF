from pymongo import ASCENDING, DESCENDING
from pymongo import MongoClient
import motor.motor_asyncio
import asyncio

connectionLocal = MongoClient('localhost', 27017)
db = connectionLocal.ETF_db

motor_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
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
arbitrage_per_min.create_index([('DateTimeOfArbitrage', DESCENDING)])
arbitrage_per_min.create_index([('ETFName', ASCENDING)])

trade_per_min_WS = db.TradePerMinWS
# trade_per_min_WS.create_index([("end_ts", DESCENDING), ("symbol", ASCENDING)], unique=True)
# trade_per_min_WS.create_index([('end_ts', DESCENDING)])
# trade_per_min_WS.create_index([('symbol', ASCENDING)])

trade_per_min_WS_motor = motor_db.TradePerMinWS

# async def create_index_for_motorcolls(coll, indexterm, order=ASCENDING):
#     await coll.create_index([indexterm,order])
# loop1 = asyncio.get_event_loop()
# task1 = asyncio.ensure_future(create_index_for_motorcolls(trade_per_min_WS_motor,'sym',ASCENDING))
# task2 = asyncio.ensure_future(create_index_for_motorcolls(trade_per_min_WS_motor,'e',DESCENDING))
# loop1.run_until_complete(task1,task2)

quotesWS_collection = db.QuotesLiveData

connectionLocal.close()
