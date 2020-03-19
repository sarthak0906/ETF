# API to get Quotes Data 
# Check if Quotes data already exsists in MongoDB, If Does fetch from MongoDb
# If Doesn't exsist fetch from polygon and save in MongoDb

# Gather quotes data in AssembleQuotesData and return 'READY' a Quotes pandas dataframe object
import sys
sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
import datetime

from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from PolygonTickData.FetchPolygonDataForUrls import FetchPolygonData
from MongoDB.StoreFetchQuotesData import MongoQuotesData
from PolygonTickData.Helper import Helper


class PolygonQuotesData(object):
	
	def fetchQuotesDataFromPolygonAPI(self, quotesRoutines=None, date=None):
		objFetchData=FetchPolygonData(date=date,PolygonMethod=PolgonDataCreateURLS().PolygonHistoricQuotes)
		finalResultDict=objFetchData.getDataFromPolygon(getUrls=quotesRoutines, finalResultDict=[])
		return pd.DataFrame(finalResultDict)[['Symbol','P','S','p','s','t','X','x']]

	def saveQuotesDataInMongoDB(self, symbol=None, dateForQuotes=None, data=None):
		objMongoQuotes = MongoQuotesData()
		savingStatus = objMongoQuotes.saveQuotesDataToMongo(symbol=symbol, dateForQuotes=dateForQuotes, data=data)
		if savingStatus:
			print("Saved Succesfully {} for {} at {}".format(symbol,dateForQuotes,datetime.datetime.now()))
		else:
			print("Error Occured While Saving {} for {} at {}".format(symbol,dateForQuotes,datetime.datetime.now()))
		
	# Check if symbol,date pair exsist in MongoDB, If don't exsist download URLs for the symbols
	def checkIfQuotesDataExsistInMongoDB(self, symbols=None, date=None):
		objMongoQuotes = MongoQuotesData()
		symbolsToBeDownloaded=[]
		for symbol in symbols:
			if not objMongoQuotes.doesItemExsistInQuotesMongoDb(symbol,date):
				symbolsToBeDownloaded.append(symbol)
		return symbolsToBeDownloaded

	def fetchQuotesDataFromMongoDB(self,symbols=None, date=None):
		objMongoQuotes = MongoQuotesData()
		data=[]
		for symbol in symbols:
			quotesDictData=objMongoQuotes.fetchDataFromQuotesData(s=symbol, date=date)
			data=data+(quotesDictData['data'])
		return pd.DataFrame(data)
		
	def createQuotesUrlsForStocks(self,symbols=None, date=None, endTs=None):
		createUrls=PolgonDataCreateURLS()
		quotesRoutines = [createUrls.PolygonHistoricQuotes(date=date, symbol=symbol,startTS=None,endTS=endTs,limitresult=str(50000)) for symbol in symbols]
		return quotesRoutines


class AssembleQuotesData(object):
	def __init__(self, symbols=None,date=None):
		self.date=date
		self.endTs=Helper().convertHumanTimeToUnixTimeStamp(date=self.date,time='17:00:00')
		self.symbols=symbols
		self.objQuotes=PolygonQuotesData()
		
	def getQuotesData(self):
		# Perform check if symbols need to be downloaded or they already exist in the DB
		symbolsToBeDownloaded = self.objQuotes.checkIfQuotesDataExsistInMongoDB(symbols=self.symbols, date=self.date)
		# Check if any symbol needs to be downloaded
		if symbolsToBeDownloaded:
			# Create URLs
			quotesRoutines=self.objQuotes.createQuotesUrlsForStocks(symbols=symbolsToBeDownloaded, date=self.date, endTs= self.endTs)
			# Fetch Data for URLs
			finalResultDf=self.objQuotes.fetchQuotesDataFromPolygonAPI(quotesRoutines=quotesRoutines, date=self.date)
			
			print("DataQuotes.py Time to Do a query over symbol in Pandas Dataframe Line 73")
			# Save the finalResultDf into MongoDb one by one for each symbol
			# This thing is taking too much time - KTZ In searching over symbol
			for symbol in symbolsToBeDownloaded:
				data=finalResultDf[finalResultDf['Symbol']==symbol]
				_ = self.objQuotes.saveQuotesDataInMongoDB(symbol=symbol, dateForQuotes=self.date, data=data)
			print("DataQuotes.py - Line 79 ")

		# Prepare to Return a dataframe for the Symbols
		return self.objQuotes.fetchQuotesDataFromMongoDB(symbols =self.symbols, date = self.date)
			
if __name__ == "__main__":
	ob=AssembleQuotesData(symbols=['XLK'],date='2020-03-13')
	quotesDataDf=ob.getQuotesData()
	print(quotesDataDf)


