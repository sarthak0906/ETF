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
from CommonServices.EmailService import EmailSender
import pandas as pd
from datetime import datetime
from datetime import timedelta
from CalculateETFArbitrage.Control import ArbitrageCalculation
from MongoDB.SaveArbitrageCalcs import SaveCalculatedArbitrage
from CalculateETFArbitrage.GetRelevantHoldings import RelevantHoldings
from MongoDB.FetchArbitrage import FetchArbitrage
import logging
import os
path = os.path.join(os.getcwd(), "Logs/")
if not os.path.exists(path):
    os.makedirs(path)

filename = path + datetime.now().strftime("%Y%m%d") + "-ArbEventLog.log"
filename2 = path + datetime.now().strftime("%Y%m%d") + "-ArbErrorLog.log"
handler = logging.FileHandler(filename)
handler2 = logging.FileHandler(filename2)
logging.basicConfig(filename=filename, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w')
# logger = logging.getLogger("EventLogger")
logger = logging.getLogger(__name__)
logger2 = logging.getLogger("ArbErrorLogger")
logger.setLevel(logging.DEBUG)
logger2.setLevel(logging.ERROR)
logger.addHandler(handler)
logger2.addHandler(handler2)

etfwhichfailed = []
# MAKE A LIST OF WORKING ETFs.
workinglist = list(pd.read_csv("WorkingETFs.csv").columns.values)
print("List of working ETFs:")
print(workinglist)
print(len(workinglist))
date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
# date = '2020-04-03'

# CHECK ARBITRAGE COLLECTION FOR ETFs ALREADY PRESENT.
arb_db_data = FetchArbitrage().fetch_arbitrage_data(date)
arb_db_data_etflist = [arbdata['ETFName'] for arbdata in arb_db_data]
arb_db_data_etflist = list(set(arb_db_data_etflist))
print("List of ETFs whose arbitrage calculation is present in DB:")
print(arb_db_data_etflist)
print(len(arb_db_data_etflist))

# REMOVE THE ETFs, FROM WORKING ETF LIST, WHOSE ARBITRAGE HAS ALREADY BEEN CALCULATED.
print("Updated etflist:")
workingset = set(workinglist)
doneset = set(arb_db_data_etflist)
etflist = list(workingset.difference(doneset))
print(etflist)
print(len(etflist))

for etfname in etflist:
    try:
        print("Doing Analysis for ETF= " + etfname)
        logger.debug("Doing Analysis for ETF= {}".format(etfname))
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
        logger2.exception(e)
        emailobj = EmailSender()
        msg = emailobj.message(subject="Exception Occurred",
                               text="Exception Caught in ETFAnalysis/CalculateETFArbitrage/Caller.py {}".format(
                                   traceback.format_exc()))
        emailobj.send(msg=msg, receivers=['piyush888@gmail.com', 'kshitizsharmav@gmail.com'])
        continue
if len(etfwhichfailed) > 0:
    RelevantHoldings().write_to_csv(etfwhichfailed, "etfwhichfailed.csv")

print(etflist)
print(etfwhichfailed)
