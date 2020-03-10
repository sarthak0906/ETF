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

	def getDataFromPolygon(self,getUrls=None,columnsNeeded=None,finalDf=None,PolygonMethod=None):
		responses=main(getUrls)
		paginatedURLS=[]

		for response in responses:
			
			start_time=time.time()
			symbol=response['ticker']
			print("Time to get Symbol--- %s seconds ---" % (time.time() - start_time))

			start_time=time.time()
			tempdf=pd.DataFrame.from_dict(response['results'])[columnsNeeded]
			print("Time to build tempdf--- %s seconds ---" % (time.time() - start_time))

			tempdf['Symbol']=symbol

			start_time=time.time()
			finalDf=finalDf.append(tempdf)
			print("Time to append to finaldf--- %s seconds ---" % (time.time() - start_time))

			start_time=time.time()
			lastUnixTimeStamp=self.helperObj.getLastTimeStamp(response)
			print("Time to get lastUnixTimeStamp--- %s seconds ---" % (time.time() - start_time))

			if self.helperObj.checkTimeStampForPagination(lastUnixTimeStamp,self.extractDataTillTime):
				paginatedURLS.append(PolygonMethod(date=self.date, symbol=symbol,startTS=str(lastUnixTimeStamp),endTS=self.endTs,limitresult=str(50000)))
				
		if len(paginatedURLS)>0:
			finalDf=self.getDataFromPolygon(getUrls=paginatedURLS,columnsNeeded=columnsNeeded,finalDf=finalDf,PolygonMethod=PolygonMethod)
		return finalDf
			
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

		tradesDataDf=pd.DataFrame(columns = ['p','s','t','x','Symbol'])
		tradesDataDf=self.getDataFromPolygon(getUrls=trade_routines,columnsNeeded=['p','s','t','x'],finalDf=tradesDataDf,PolygonMethod=Polygonobj.PolygonHistoricTrades)
		print(tradesDataDf)
		print(tradesDataDf['Symbol'].unique())
		
		quotesDataDf=pd.DataFrame(columns = ['P','S','p','s','t','X','x','Symbol'])
		quotesDataDf=self.getDataFromPolygon(getUrls=quotes_routines,columnsNeeded=['P','S','p','s','t','X','x'],finalDf=quotesDataDf,PolygonMethod=Polygonobj.PolygonHistoricQuotes)
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






