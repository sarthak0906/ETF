import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ

from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from PolygonTickData.Helper import Helper
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
from CommonServices.ThreadingRequests import IOBoundThreading
from CommonServices.MultiProcessingTasks import CPUBonundThreading

import logging
import asyncio
import datetime
import pandas as pd
import sys
import time

class PolygonResponseStorage(object):
    __slots__ = ('symbol', 'data','paginatedRequest')
    def __init__(self, symbol=None, data=None, paginatedRequest=None):
        self.symbol = symbol
        self.data = data
        self.paginatedRequest=paginatedRequest
        
class FetchPolygonData(object):
	
	def __init__(self, date=None, previousdate=None, starttime='9:00:00', endtime='17:00:00', endtimeLoop='16:00:00', PolygonMethod=None):
		self.helperObj = Helper()
		self.date = date
		self.starttime = starttime  # 9 AM
		self.endtime = endtime  # 5 PM
		self.endtimeLoop = endtimeLoop  # 4 PM
		self.extractDataTillTime = self.helperObj.stringTimeToDatetime(date=self.date, time=self.endtimeLoop)
		self.endTs=self.helperObj.convertHumanTimeToUnixTimeStamp(date=self.date,time=self.endtime)
		self.PolygonMethod=PolygonMethod

		
	def __extractDataFromResponse(self,response):
		symbol=response['ticker']
		print("Symbol being processed "+symbol)
		
		lastUnixTimeStamp=self.helperObj.getLastTimeStamp(response)
		paginatedRequest=None
		if self.helperObj.checkTimeStampForPagination(lastUnixTimeStamp,self.extractDataTillTime):
			# Create new urls for pagination request
			paginatedRequest = self.PolygonMethod(date=self.date, symbol=symbol,startTS=str(lastUnixTimeStamp),endTS=self.endTs,limitresult=str(50000))
		
		# Creating an efficient storage object with PolygonResponseStorage for returning 
		PoReObj=PolygonResponseStorage(symbol=symbol, data=response['results'], paginatedRequest=paginatedRequest)
		return PoReObj
		
	def getDataFromPolygon(self,getUrls=None, storeDataInMongo=None):
		# Calling IO Bound Threading to fetch data for URLS
		responses=IOBoundThreading(getUrls)
		# Calling CPU Bound Threading to proess the responses from URLS
		threadingResults=CPUBonundThreading(self.__extractDataFromResponse,responses)
		paginatedURLS=[]
		for result in threadingResults:
			# Store Data In MongoDB
			_ = storeDataInMongo( symbol=result.symbol, datetosave=self.date, savedata=result.data)
			if result.paginatedRequest:
				paginatedURLS.append(result.paginatedRequest)
		
		# Check if we need to do pagination for results, if Yes we do a recursion call to getDataFromPolygon
		if len(paginatedURLS)>0:
			_ = self.getDataFromPolygon(getUrls=paginatedURLS,storeDataInMongo=storeDataInMongo)
		
		return True
			
	'''
	# Pass here etfdata object
	def assemblePolygonData(self,symbols):
	# Objects for polygon requests
		Polygonobj = PolgonDataCreateURLS()
		# Get all tickers for the ETF
		trade_routines = [Polygonobj.PolygonHistoricTrades(date=self.date, symbol=symbol,startTS=None,endTS=self.endTs,limitresult=str(50000)) for symbol in symbols]
		quotes_routines = [Polygonobj.PolygonHistoricQuotes(date=self.date, symbol=symbol,startTS=None,endTS=self.endTs,limitresult=str(50000)) for symbol in ['XLK']]
		openCloseURLs =[Polygonobj.PolygonDailyOpenClose(date=self.date, symbol=symbol) for symbol in symbols]

		#tradesDataDf=pd.DataFrame(columns = ['p','s','t','x','Symbol'])
		# p : TradePrice, s : TradeSie, t :Timestamp, x: Exchange
		self.PolygonMethod=Polygonobj.PolygonHistoricTrades
		tradesDataDf=self.getDataFromPolygon(getUrls=trade_routines,finalResultDict=[])
		tradesDataDf=pd.DataFrame(tradesDataDf)[['Symbol','p','s','t','x']]
		print(tradesDataDf)
		print(tradesDataDf['Symbol'].unique())
		
		#quotesDataDf=pd.DataFrame(columns = ['P','S','p','s','t','X','x','Symbol'])
		self.PolygonMethod=Polygonobj.PolygonHistoricQuotes
		quotesDataDf=self.getDataFromPolygon(getUrls=quotes_routines,finalResultDict=[])
		quotesDataDf=pd.DataFrame(quotesDataDf)[['Symbol','P','S','p','s','t','X','x']]
		print(quotesDataDf)
		print(quotesDataDf['Symbol'].unique())
		
		priceforNAVfilling=self.getOpenCloseData(openCloseURLs=openCloseURLs)
		print(priceforNAVfilling)

		return tradesDataDf, quotesDataDf, priceforNAVfilling
	'''

