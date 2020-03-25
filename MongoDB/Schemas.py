from pymongo import ASCENDING, DESCENDING
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.ETF_db

# Quotes Pipeline
quotesCollection = db.QuotesData
quotesCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])
quotespipeline =[
{'$match':  ''},
{'$unwind': '$data'},
{'$group': {
    '_id':'$_id',
    'data':{'$push':{
    'Symbol':'$data.Symbol',
    'Time':'$data.t',
    'Bid Price':'$data.p',
    'Bid Size':'$data.s',
    'Ask Price':'$data.P',
    'Ask Size':'$data.S',
        }}
    }}
]

# Trades Pipeline
tradeCollection = db.TradesData
tradeCollection.create_index([("dateForData", DESCENDING), ("symbol", ASCENDING)])
tradespipeline =[
{'$match':  ''},
{'$unwind': '$data'},
{'$group': {
    '_id':'$_id',
    'data':{'$push':{
    'Symbol':'$data.Symbol',
    'Time':'$data.t',
    'Trade Price':'$data.vw',
    'Trade Size':'$data.v',
    'Number of Trades':'$data.n',
        }}
    }}
]

# Daily Open Close Collection
dailyopencloseCollection=db.DailyOpenCloseCollection
dailyopencloseCollection.create_index([("dateForData", DESCENDING), ("Symbol", ASCENDING)])

# Arbitrage
arbitragecollection = db.ArbitrageCollection
arbitragecollection.create_index([("dateOfAnalysis", DESCENDING), ("ETFName", ASCENDING)])



