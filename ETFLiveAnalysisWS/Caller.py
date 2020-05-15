import sys, traceback
# For Piyush System
sys.path.extend(['/home/piyush/Desktop/etf1903', '/home/piyush/Desktop/etf1903/ETFsList_Scripts',
                 '/home/piyush/Desktop/etf1903/HoldingsDataScripts',
                 '/home/piyush/Desktop/etf1903/CommonServices',
                 '/home/piyush/Desktop/etf1903/CalculateETFArbitrage','/home/piyush/Desktop/etf1903/ETFLiveAnalysis'])
# For Production env
sys.path.extend(['/home/ubuntu/ETFAnalysis', '/home/ubuntu/ETFAnalysis/ETFsList_Scripts',
                 '/home/ubuntu/ETFAnalysis/HoldingsDataScripts', '/home/ubuntu/ETFAnalysis/CommonServices',
                 '/home/ubuntu/ETFAnalysis/CalculateETFArbitrage'])
sys.path.append("..")  # Remove in production - KTZ
import datetime
import time
import schedule
from statistics import mean
import pandas as pd
import numpy as np
from ETFLiveAnalysisWS.CalculatePerMinArb import ArbPerMin
from MongoDB.PerMinDataOperations import PerMinDataOperations
from PolygonTickData.Helper import Helper

class PerMinAnalysis():
    def handleQuotesResponse(self, result):
        try:
            return (result['sym'], (result['ap'] - result['bp']))
        except:
            return (result['sym'],None)

    def PerMinAnalysisCycle(self, obj):
        starttime = time.time()
        print("Start Time : {}".format(starttime))
        # ETF Arbitrage Calculation
        #######################################################
        startarb = time.time()
        arbDF = pd.DataFrame.from_dict(obj.calcArbitrage(), orient='index', columns=['Arbitrage'])
        endarb = time.time()
        print("Arbitrage time: {}".format(endarb - startarb))
        #######################################################

        # UTC Timestamps for pulling data from QuotesLiveData DB, below:
        #######################################################
        end_dt = datetime.datetime.now().replace(second=0, microsecond=0)
        end_dt_ts = int(end_dt.timestamp() * 1000)
        print("End dt ts: {}".format(end_dt_ts))
        start_dt = end_dt - datetime.timedelta(minutes=1)
        startts = int(start_dt.timestamp() * 1000)
        print("start ts: {}".format(startts))
        #######################################################

        #ETF Spread Calculation
        #######################################################
        startspread = time.time()
        QuotesResults = PerMinDataOperations().FetchQuotesLiveDataForSpread(startts, end_dt_ts)
        spread_list = [self.handleQuotesResponse(result) for result in QuotesResults]
        spreadDF = pd.DataFrame(spread_list, columns=['symbol', 'Spread'])
        if not spreadDF.empty:
            spreadDF = spreadDF.groupby(['symbol']).mean()
        else:
            spreadDF.set_index('symbol', inplace=True)
        endspread = time.time()
        print("Spread Time: {}".format(endspread - startspread))
        #######################################################

        # Results:
        #######################################################
        print("Arb DF:")
        print(arbDF)
        print("Spread DF:")
        print(spreadDF)
        mergeDF = arbDF.merge(spreadDF, how='outer', left_index=True, right_index=True)
        print("Merged DF:")
        print(mergeDF)
        endtime = time.time()
        print("One whole Cycle time : {}".format(endtime - starttime))
        #######################################################

# obj = ArbPerMin()
# while True:
#     starttime = time.time()
#     dt = datetime.datetime.now() + datetime.timedelta(minutes=1)
#     startarb = time.time()
#     arbDF = pd.DataFrame.from_dict(obj.calcArbitrage(), orient='index',columns=['Arbitrage'])
#     endarb = time.time()
#     print("Arbitrage time: {}".format(endarb-startarb))
#     # UTC Timestamps below.
#     end_dt = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(hours=20)
#     end_dt_ts = int(end_dt.timestamp()*1000)
#     start_dt = end_dt - datetime.timedelta(minutes=1)
#     startts = int(start_dt.timestamp()*1000)
#
#     startspread =time.time()
#     etflist = list(pd.read_csv("WorkingETFs.csv").columns.values)
#
#     QuotesResults = PerMinDataOperations().FetchQuotesLiveDataForSpread(startts, end_dt_ts)
#     spread_list = [(result['sym'], (result['ap']-result['bp'])) for result in QuotesResults]
#     spreadDF = pd.DataFrame(spread_list, columns=['symbol','Spread'])
#     if not spreadDF.empty:
#         spreadDF = spreadDF.groupby(['symbol']).mean()
#     endspread = time.time()
#     print("Spread Time: {}".format(endspread-startspread))
#
#     print("Arb DF:")
#     print(arbDF)
#     print("Spread DF:")
#     print(spreadDF)
#     mergeDF = arbDF.merge(spreadDF, how='outer',left_index=True, right_index=True)
#     print("Merged DF:")
#     print(mergeDF)
#     endtime = time.time()
#     print("One whole Cycle time : {}".format(endtime-starttime))
#     while datetime.datetime.now() < dt:
#         time.sleep(1)

if __name__=='__main__':
    # Object life to be maintained throughout the day while market is open
    ArbCalcObj = ArbPerMin()
    PerMinAnlysObj = PerMinAnalysis()
    schedule.every(1).minutes.do(PerMinAnlysObj.PerMinAnalysisCycle, ArbCalcObj)
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)




