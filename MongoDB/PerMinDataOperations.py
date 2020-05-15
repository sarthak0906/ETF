import datetime
from MongoDB.Schemas import trade_per_min_WS_motor, trade_per_min_WS, quotesWS_collection
# from ETFLiveAnalysisWS import PollingOperation

class PerMinDataOperations():

    async def do_insert(self,data):
        result = await trade_per_min_WS_motor.insert_many(data)
        print('inserted %d docs' % (len(result.inserted_ids),))
        # if result:
        #     PollingOperation.pollvar = PollingOperation.pollvar + 1
        # print(PollingOperation.pollvar)

    # def  insertDataPerMin(self, responseDict):
    #     # print("Saving {} into Trade Per Min Collection...".format(responseDict['sym']))
    #     # trade_per_min_WS.insert_one(responseDict)
    #     trade_per_min_WS.insert_many(responseDict, ordered=False)

    def  insertQuotesLive(self, quotesData):
        # print("Saving {} into Trade Per Min Collection...".format(responseDict['sym']))
        # trade_per_min_WS.insert_one(responseDict)
        quotesWS_collection.insert_many(quotesData, ordered=False)

    def FetchAllTradeDataPerMin(self, DateTimeOfTrade):
        dt = datetime.datetime.strptime(DateTimeOfTrade, '%Y-%m-%d %H:%M')
        dt_ts = int(dt.timestamp()*1000)
        all_tickers_data = trade_per_min_WS.find({'e':dt_ts},{'_id':0,'sym':1,'vw':1})
        return all_tickers_data

    def FetchQuotesLiveDataForSpread(self, startts, endts):
        quotes_data_for_etf = quotesWS_collection.find({'t':{'$gt':startts, '$lte':endts}},{'sym':1,'ap':1,'bp':1})
        return quotes_data_for_etf


