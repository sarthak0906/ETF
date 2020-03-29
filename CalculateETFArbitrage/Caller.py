import sys  # Remove in production - KTZ
import traceback

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
from datetime import datetime
from CalculateETFArbitrage.Control import ArbitrageCalculation
from MongoDB.SaveArbitrageCalcs import SaveCalculatedArbitrage
from CalculateETFArbitrage.GetRelevantHoldings import RelevantHoldings
import csv


etfwhichfailed=[]
etflist = list(pd.read_csv("NonChineseETFs.csv").columns.values)
etflist=etflist[etflist.index('IBB'):]
print(etflist)
print(len(etflist))
# etflist = ['XLK','XLY', 'XLC', 'VCR', 'ITB', 'IYC', 'FDIS', 'XRT', 'FXD']
etflist = ['XLK','VGT','IYW','FTEC']
date = '2020-03-17'

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
                                                        dateWhenAnalysisRan=datetime.now().date(),
                                                        data=data.to_dict(orient='records'),
                                                        dateofAnalysis=datetime.strptime(date, '%Y-%m-%d'))
            
    except Exception as e:
        etfwhichfailed.append(etfname)
        print("exception in {} etf, not crawled".format(etfname))
        print(e)
        traceback.print_exc()
        continue

print(etflist)
print(etfwhichfailed)