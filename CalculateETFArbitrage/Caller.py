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
import logging
import os
path = os.path.join(os.getcwd(), "Logs/")
if not os.path.exists(path):
    os.makedirs(path)
filename = path + "ArbCalcLog.log"
handler = logging.FileHandler(filename)
logging.basicConfig(filename=filename, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(handler)

etfwhichfailed = []
etflist = list(pd.read_csv("WorkingETFs.csv").columns.values)
print(etflist)
print(len(etflist))
date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

for etfname in etflist:
    try:
        print("Doing Analysis for ETF= " + etfname)
        logger.debug("Doing Analysis for ETF= " + etfname)
        data = ArbitrageCalculation().calculateArbitrage(etfname, date)

        if data is None:
            print("Holding Belong to some other Exchange, No data was found")
            logger.debug("Holding Belong to some other Exchange, No data was found for {}".format(etfname))
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
        logger.exception(e)
        continue
if len(etfwhichfailed) > 0:
    RelevantHoldings().write_to_csv(etfwhichfailed, "etfwhichfailed.csv")

print(etflist)
print(etfwhichfailed)
