import sys  # Remove in production - KTZ
import traceback
# For Piyush System
sys.path.extend(['/home/piyush/Desktop/etf1903', '/home/piyush/Desktop/etf1903/ETFsList_Scripts',
                 '/home/piyush/Desktop/etf1903/HoldingsDataScripts',
                 '/home/piyush/Desktop/etf1903/CommonServices',
                 '/home/piyush/Desktop/etf1903/CalculateETFArbitrage'])
# For Production env
sys.path.extend(['/home/ubuntu/ETFAnalysis', '/home/ubuntu/ETFAnalysis/ETFsList_Scripts',
                 '/home/ubuntu/ETFAnalysis/HoldingsDataScripts', '/home/ubuntu/ETFAnalysis/CommonServices',
                 '/home/ubuntu/ETFAnalysis/CalculateETFArbitrage'])
sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
from datetime import datetime
from datetime import timedelta
from CalculateETFArbitrage.Control import ArbitrageCalculation
from MongoDB.SaveArbitrageCalcs import SaveCalculatedArbitrage
from CalculateETFArbitrage.GetRelevantHoldings import RelevantHoldings
import csv

etfwhichfailed = []
etflist = list(pd.read_csv("WorkingETFs.csv").columns.values)
# etflist = ['XLK','BNKU', 'NUGT', 'BNKD', 'NRGO', 'CWEB', 'JNUG', 'NRGU', 'NRGD', 'VMOT']
# etflist = ['NUGT', 'CWEB', 'JNUG']
print(etflist)
print(len(etflist))
date = (datetime.now()-timedelta(days = 1)).strftime("%Y-%m-%d")

for etfname in etflist:
    try:
        print("Doing Analysis for ETF= " + etfname)
        data = ArbitrageCalculation().calculateArbitrage(etfname, date)

        if data is None:
            print("Holding Belong to some other Exchange, No data was found")
            etfwhichfailed.append(etfname)
            continue
        else:
            data.reset_index(inplace=True)
            SaveCalculatedArbitrage().insertIntoCollection(ETFName=etfname,
                                                           dateOfAnalysis=datetime.strptime(date, '%Y-%m-%d'),
                                                           data=data.to_dict(orient='records'),
                                                           dateWhenAnalysisRan=datetime.now()
                                                           )

    except Exception as e:
        etfwhichfailed.append(etfname)
        print("exception in {} etf, not crawled".format(etfname))
        print(e)
        traceback.print_exc()
        continue
if len(etfwhichfailed) > 0:
    RelevantHoldings().write_to_csv(etfwhichfailed, "etfwhichfailed.csv")

print(etflist)
print(etfwhichfailed)
