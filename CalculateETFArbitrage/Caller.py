import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
from datetime import datetime
from CalculateETFArbitrage.Control import ArbitrageCalculation
from MongoDB.SaveArbitrageCalcs import SaveCalculatedArbitrage
from CalculateETFArbitrage.GetRelevantHoldings import RelevantHoldings
import csv

try:
    # etflist = []
    # with open('NonChineseETFs.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         etflist.extend(row)
    # print(etflist)
    # print(len(etflist))
    # etflist = ['XLK','XLY', 'XLC', 'VCR', 'ITB', 'IYC', 'FDIS', 'XRT', 'FXD']
    etflist = ['XLK','QQQ']
    date = '2020-03-17'
    for etfname in etflist:
        data = ArbitrageCalculation().calculateArbitrage(etfname, date)
        data.reset_index(inplace=True)
        SaveCalculatedArbitrage().insertIntoCollection(etfname, datetime.now().date().strftime('%Y-%m-%d'),
                                                       data.to_dict(orient='records'))
except Exception as e:
    print("exception in {} etf".format(etfname))
    print(e)
