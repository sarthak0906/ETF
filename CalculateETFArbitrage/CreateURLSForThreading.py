import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ

from PolygonTickData.PolygonDataAPIConnection2 import PolgonData
from helper import Helper
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
from ThreadingRequests import main

import logging
import asyncio
import datetime
import pandas as pd
import sys
import time

class EtfData(object):
    __slots__ = ('symbol', 'data')
    def __init__(self, sybl, dt):
        self.symbol = sybl
        self.data = dt

class CallPolygonApi(object):
	
	def __init__(self, date=None, previousdate=None, starttime='9:00:00', endtime='17:00:00', endtimeLoop='16:00:00'):
		self.helperObj = Helper()
		self.date = date
		self.starttime = starttime  # 9 AM
		self.endtime = endtime  # 5 PM
		self.endtimeLoop = endtimeLoop  # 4 PM
		self.extractDataTillTime = self.helperObj.stringTimeToDatetime(date=self.date, time=self.endtimeLoop)
		self.endTs=self.helperObj.convertHumanTimeToUnixTimeStamp(date=self.date,time=self.endtime)
		self.tickHistDataQuotes = None
		self.tickHistDataTrade = None
		self.priceforNAVfilling = None

	def getDataFromPolygon(self,getUrls=None,finalResultDict=None,PolygonMethod=None):
		responses=main(getUrls)
		paginatedURLS=[]
		for response in responses:
			
			start_time=time.time()
			symbol=response['ticker']
			print("Time to get Symbol--- %s seconds ---" % (time.time() - start_time))
			
			start_time=time.time()
			result = [dict(item, **{'Symbol':symbol}) for item in response['results']]
			print("Time to append symbol to dict elements --- %s seconds ---" % (time.time() - start_time))

			start_time=time.time()
			finalResultDict=finalResultDict+result
			print("Time to append to list finalResultDict--- %s seconds ---" % (time.time() - start_time))

			start_time=time.time()
			lastUnixTimeStamp=self.helperObj.getLastTimeStamp(response)
			print("Time to get lastUnixTimeStamp--- %s seconds ---" % (time.time() - start_time))

			if self.helperObj.checkTimeStampForPagination(lastUnixTimeStamp,self.extractDataTillTime):
				paginatedURLS.append(PolygonMethod(date=self.date, symbol=symbol,startTS=str(lastUnixTimeStamp),endTS=self.endTs,limitresult=str(50000)))
		
		if len(paginatedURLS)>0:
			finalResultDict=self.getDataFromPolygon(getUrls=paginatedURLS,finalResultDict=finalResultDict,PolygonMethod=PolygonMethod)
		
		return finalResultDict
			
	def getOpenCloseData(self,openCloseURLs=None):
		responses=main(openCloseURLs)
		priceforNAVfilling={}
		for response in responses:
			priceforNAVfilling[response['symbol']] = response['open']
		return priceforNAVfilling

	# Pass here etfdata object
	def assemblePolygonData(self,symbols):
	# Objects for polygon requests
		Polygonobj = PolgonData()
		# Get all tickers for the ETF
		trade_routines = [Polygonobj.PolygonHistoricTrades(date=self.date, symbol=symbol,startTS=None,endTS=self.endTs,limitresult=str(50000)) for symbol in symbols]
		quotes_routines = [Polygonobj.PolygonHistoricQuotes(date=self.date, symbol=symbol,startTS=None,endTS=self.endTs,limitresult=str(50000)) for symbol in ['XLK']]
		openCloseURLs =[Polygonobj.PolygonDailyOpenClose(date=self.date, symbol=symbol) for symbol in symbols]

		#tradesDataDf=pd.DataFrame(columns = ['p','s','t','x','Symbol'])
		tradesDataDf=self.getDataFromPolygon(getUrls=trade_routines,finalResultDict=[],PolygonMethod=Polygonobj.PolygonHistoricTrades)
		tradesDataDf=pd.DataFrame(tradesDataDf)[['Symbol','p','s','t','x']]
		print(tradesDataDf)
		print(tradesDataDf['Symbol'].unique())
		
		#quotesDataDf=pd.DataFrame(columns = ['P','S','p','s','t','X','x','Symbol'])
		quotesDataDf=self.getDataFromPolygon(getUrls=quotes_routines,finalResultDict=[],PolygonMethod=Polygonobj.PolygonHistoricQuotes)
		quotesDataDf=pd.DataFrame(quotesDataDf)[['Symbol','P','S','p','s','t','X','x']]
		print(quotesDataDf)
		print(quotesDataDf['Symbol'].unique())
		
		priceforNAVfilling=self.getOpenCloseData(openCloseURLs=openCloseURLs)
		print(priceforNAVfilling)

		return tradesDataDf, quotesDataDf, priceforNAVfilling


''''
if __name__ == "__main__":
	# Create an object of date when we need and time between which we need data
	previousdate = '2020-03-08'
	date = '2020-03-09'
	starttime = '9:30:00'
	endtime = '17:00:00'
	endtimeLoop = '16:00:00'
	etfname = 'XLK'

	etfData = LoadHoldingsdata(etfname=etfname, fundholdingsdate='20200226')

	polygonApi=CallPolygonApi(date=date)
	polygonApi.assemblePolygonData(etfData.getSymbols())
'''






