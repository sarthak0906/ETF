import datetime
from MongoDB.Schemas import trade_per_min_WS_motor, trade_per_min_WS, quotesWS_collection


class PerMinDataOperations():

    async def do_insert(self,data):
        result = await trade_per_min_WS_motor.insert_many(data)
        print('inserted %d docs' % (len(result.inserted_ids),))

    # def  insertDataPerMin(self, responseDict):
    #     # print("Saving {} into Trade Per Min Collection...".format(responseDict['sym']))
    #     # trade_per_min_WS.insert_one(responseDict)
    #     trade_per_min_WS.insert_many(responseDict, ordered=False)

    def  insertQuotesLive(self, quotesData):
        # print("Saving {} into Trade Per Min Collection...".format(responseDict['sym']))
        # trade_per_min_WS.insert_one(responseDict)
        quotesWS_collection.insert_many(quotesData, ordered=False)

    def FetchAllTradeDataPerMin(self, DateTimeOfTrade):
        all_tickers_data = trade_per_min_WS.find({'e':int((datetime.datetime.strptime(DateTimeOfTrade, '%Y-%m-%d %H:%M').replace(tzinfo=datetime.timezone.utc).timestamp())*1000)},{'_id':0})
        return all_tickers_data

    def FetchQuotesLiveDataForSpread(self, etf, startts, endts):
        quotes_data_for_etf = quotesWS_collection.find({'sym':etf, 't':{'$gt':startts, '$lte':endts}},{'ap':1,'bp':1})
        return quotes_data_for_etf


