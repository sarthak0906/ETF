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

class FetchPolygonData(object):

	def __init__(self, date=None, previousdate=None, starttime='9:00:00', endtime='17:00:00', endtimeLoop='16:00:00',
				 PolygonMethod=None, insertIntoCollection=None, symbolStatus=None, CollectionName=None):
		self.helperObj = Helper()
		self.date = date
		self.starttime = starttime  # 9 AM
		self.endtime = endtime  # 5 PM
		self.endtimeLoop = endtimeLoop  # 4 PM
		self.extractDataTillTime = self.helperObj.stringTimeToDatetime(date=self.date, time=self.endtimeLoop)
		self.endTs = self.helperObj.convertHumanTimeToUnixTimeStamp(date=self.date, time=self.endtime)
		self.PolygonMethod = PolygonMethod
		self.insertIntoCollection = insertIntoCollection
		self.CollectionName=CollectionName
		self.symbolStatus=symbolStatus

	def __extractDataFromResponse(self, response):
		PaginationRequest=None
		symbol = response['ticker']
		print("Symbol being processed " + symbol)
		responseData = [dict(item, **{'Symbol':symbol}) for item in response['results']]
		lastUnixTimeStamp = self.helperObj.getLastTimeStamp(response)
		if self.helperObj.checkTimeStampForPagination(lastUnixTimeStamp, self.extractDataTillTime):
			# Create new urls for pagination request
			PaginationRequest=self.PolygonMethod(date=self.date, symbol=symbol, startTS=str(lastUnixTimeStamp),
												  endTS=self.endTs, limitresult=str(50000))
			self.symbolStatus[symbol]['batchSize'] += 1
		# Creating an efficient storage object with PolygonResponseStorage for returning
		_ = self.insertIntoCollection(symbol=symbol, datetosave=self.date, savedata=responseData,CollectionName=self.CollectionName, batchSize=self.symbolStatus[symbol]['batchSize'])
		
		if PaginationRequest:
			return PaginationRequest 
		else:
			print("No Pagination Required for = " + symbol)

	def getDataFromPolygon(self, getUrls=None):
		# Calling IO Bound Threading to fetch data for URLS
		responses = IOBoundThreading(getUrls)
		# Calling CPU Bound Threading to proess the responses from URLS
		PaginationRequest = CPUBonundThreading(self.__extractDataFromResponse, responses)
		print(PaginationRequest)
		# Check if we need to do pagination for results, if Yes we do a recursion call to getDataFromPolygon
		if len(PaginationRequest) > 0:
			_ = self.getDataFromPolygon(getUrls=PaginationRequest)
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
