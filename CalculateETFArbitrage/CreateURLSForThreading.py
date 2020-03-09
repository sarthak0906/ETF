import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ
from PolygonTickData.PolygonDataAPIConnection import PolgonData
from helper import Helper
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata

from ThreadingRequests import main

previousdate = '2020-02-25'
date = '2020-02-26'
starttime = '9:30:00'
endtime = '17:00:00'
endtimeLoop = '16:00:00'
etfname = 'XLK'

polygobj=PolgonData()
helperObj=Helper()

startTs=helperObj.convertHumanTimeToUnixTimeStamp(date,starttime)
endTs=helperObj.convertHumanTimeToUnixTimeStamp(date,endtime)

etfData = LoadHoldingsdata(etfname=etfname, fundholdingsdate='20200226')
print(etfData.getSymbols())

co_routines = [polygobj.PolygonHistoricQuotes(date=date, symbol=symbol,startTS=None,endTS=endTs,limitresult=str(5000)) for symbol in symbols]
main(co_routines)
