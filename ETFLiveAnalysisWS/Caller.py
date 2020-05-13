import datetime
import time
from statistics import mean
import pandas as pd
from ETFLiveAnalysisWS.CalculatePerMinArb import ArbPerMin
from MongoDB.PerMinDataOperations import PerMinDataOperations
from PolygonTickData.Helper import Helper

obj = ArbPerMin()
# for dt in ['2020-05-11 16:18', '2020-05-11 16:19', '2020-05-11 16:20', '2020-05-11 16:21', '2020-05-11 16:22',
#            '2020-05-11 16:23', '2020-05-11 16:24', '2020-05-11 16:25', '2020-05-11 16:26', '2020-05-11 16:27',
#            '2020-05-11 16:28', '2020-05-11 16:29', '2020-05-11 16:30', '2020-05-11 16:31', '2020-05-11 16:31',
#            '2020-05-11 16:32', '2020-05-11 16:33', '2020-05-11 16:34', '2020-05-11 16:35', '2020-05-11 16:36',
#            '2020-05-11 16:37', '2020-05-11 16:38', '2020-05-11 16:39', '2020-05-11 16:40', '2020-05-11 16:41',
#            '2020-05-11 16:42', '2020-05-11 16:43', '2020-05-11 16:44', '2020-05-11 16:45', '2020-05-11 16:46',
#            '2020-05-11 16:47', '2020-05-11 16:48', '2020-05-11 16:49', '2020-05-11 16:50', '2020-05-11 16:51',
#            '2020-05-11 16:52', '2020-05-11 16:53', '2020-05-11 16:54', '2020-05-11 16:55', '2020-05-11 16:56',
#            '2020-05-11 16:57', '2020-05-11 16:58', '2020-05-11 16:59', '2020-05-11 17:00', '2020-05-11 17:01',
#            '2020-05-11 17:02', '2020-05-11 17:03', '2020-05-11 17:04', '2020-05-11 17:05', '2020-05-11 17:06',
#            '2020-05-11 17:07', '2020-05-11 17:08', '2020-05-11 17:09', '2020-05-11 17:10', '2020-05-11 17:11',
#            '2020-05-11 17:12', '2020-05-11 17:13', '2020-05-11 17:14', '2020-05-11 17:15', '2020-05-11 17:16',
#            '2020-05-11 17:17', '2020-05-11 17:18' ]:
#     print(pd.DataFrame.from_dict(obj.calcArbitrage(dt), orient='index'))
while True:
    while True:
        dt = datetime.datetime.now() + datetime.timedelta(minutes=1)
        arbDF = pd.DataFrame.from_dict(obj.calcArbitrage(), orient='index',columns=['Arbitrage'])
        endts = int((datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).timestamp())*1000)
        startts = int((datetime.datetime.now() - datetime.timedelta(minutes=1)).replace(tzinfo=datetime.timezone.utc).timestamp()*1000)
        etflist = list(pd.read_csv("/home/piyush/Desktop/etf1903/ETFLiveAnalysisWS/WorkingETFs.csv").columns.values)
        spread_list = []
        for etf in etflist:
            startl = time.time()
            try:
                results = PerMinDataOperations().FetchQuotesLiveDataForSpread(etf, startts, endts)
                spread_for_etf = mean([res['ap']-res['bp'] for res in results])
                print(spread_for_etf)
                spread_list.append({etf:spread_for_etf})
            except Exception as e:
                pass
            endl = time.time()
            print("One iteration time : {}".format(endl-startl))
        # spreadDF = pd.DataFrame(spread_list, columns=['symbol', 'Spread'])
        # spreadDF.set_index('symbol', inplace = True)
        print("Arb DF:")
        print(arbDF)
        print("Spread DF:")
        print(startts)
        print(endts)
        print(spread_list)
        while datetime.datetime.now() < dt:
            time.sleep(1)
