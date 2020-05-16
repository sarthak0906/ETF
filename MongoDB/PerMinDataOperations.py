import datetime
from MongoDB.Schemas import trade_per_min_WS_motor, trade_per_min_WS, quotesWS_collection

class PerMinDataOperations():

    # Use AsyncIOMotorCursor for inserting into TradePerMinWS Collection
    async def do_insert(self,data):
        result = await trade_per_min_WS_motor.insert_many(data)
        print('inserted %d docs' % (len(result.inserted_ids),))

    # Insert into QuotesLiveData Collection
    def  insertQuotesLive(self, quotesData):
        quotesWS_collection.insert_many(quotesData, ordered=False)

    # Use PyMongo Cursor for fetching from TradePerMinWS Collection
    def FetchAllTradeDataPerMin(self, DateTimeOfTrade):
        dt = datetime.datetime.strptime(DateTimeOfTrade, '%Y-%m-%d %H:%M')
        dt_ts = int(dt.timestamp()*1000)
        all_tickers_data = trade_per_min_WS.find({'e':dt_ts},{'_id':0,'sym':1,'vw':1})
        return all_tickers_data

    # Fetch from QuotesLiveData Collection
    def FetchQuotesLiveDataForSpread(self, startts, endts):
        quotes_data_for_etf = quotesWS_collection.find({'t':{'$gt':startts, '$lte':endts}},{'sym':1,'ap':1,'bp':1})
        return quotes_data_for_etf


