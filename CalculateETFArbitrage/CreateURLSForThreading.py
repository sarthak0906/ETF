import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ

from PolygonTickData.PolygonDataAPIConnection2 import PolgonData
from helper import Helper
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
from ThreadingRequests import main

import logging
import asyncio
import datetime

class CallPolygonApi(object):
	
	def __init__(self, date=None, previousdate=None, starttime='9:00:00', endtime='17:00:00', endtimeLoop='16:00:00'):
		self.helperObj = Helper()
		self.date = date
		self.starttime = starttime  # 9 AM
		self.endtime = endtime  # 5 PM
		self.endtimeLoop = endtimeLoop  # 4 PM
		
		self.tickHistDataQuotes = None
		self.tickHistDataTrade = None
		self.priceforNAVfilling = None


	def getDataFromPolygon(self,getUrls):
		responses=main(getUrls)
		c=0
		for response in responses:
			print(self.helperObj.getLastTimeStamp(response))
			c+=1
			print(c)
			print(response['results'][0])

	
	# Pass here etfdata object
	def assemblePolygonData(self,symbols):
	# Objects for polygon requests
		Polygonobj = PolgonData()
		# Get all tickers for the ETF
		endTs=self.helperObj.convertHumanTimeToUnixTimeStamp(date=self.date,time=self.endtime)

		trade_routines = [Polygonobj.PolygonHistoricTrades(date=self.date, symbol=symbol,startTS=None,endTS=endTs,limitresult=str(5000)) for symbol in symbols]
		quotes_routines = [Polygonobj.PolygonHistoricQuotes(date=self.date, symbol=symbol,startTS=None,endTS=endTs,limitresult=str(5000)) for symbol in symbols]
		openclose_routines =[Polygonobj.PolygonDailyOpenClose(date=self.date, symbol=symbol) for symbol in symbols]

		print("Trades Data")
		self.getDataFromPolygon(trade_routines)
		'''
		print("Quotes Data")
		self.getDataFromPolygon(quotes_routines)
		print("Open Close Data")
		self.getDataFromPolygon(openclose_routines)
		'''


if __name__ == "__main__":
	# Create an object of date when we need and time between which we need data
	previousdate = '2020-02-25'
	date = '2020-02-26'
	starttime = '9:30:00'
	endtime = '17:00:00'
	endtimeLoop = '16:00:00'
	etfname = 'XLK'

	etfData = LoadHoldingsdata(etfname=etfname, fundholdingsdate='20200226')

	polygonApi=CallPolygonApi(date=date)
	polygonApi.assemblePolygonData(etfData.getSymbols())







