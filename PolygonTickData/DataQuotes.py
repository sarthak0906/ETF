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
		
	# Checks if quotes data already exsists for the symbol and date
	def checkIfQuotesDataExsistInMongoDB(self, symbol=None, date=None):
		objMongoQuotes = MongoQuotesData()
		return objMongoQuotes.doesItemExsistInQuotesMongoDb(symbol,date)
	
	def fetchQuotesDataFromMongoDBIfExsist(self):
		pass

	def createQuotesUrlsForStocks(self,symbols=None, date=None, endTs=None):
		quotesRoutines=[]
		createUrls=PolgonDataCreateURLS()
		for symbol in symbols:
			if not self.checkIfQuotesDataExsistInMongoDB(symbol,date):
					quotesRoutines.append(createUrls.PolygonHistoricQuotes(date=date, symbol=symbol,startTS=None,endTS=endTs,limitresult=str(50000)))
		return quotesRoutines


class AssembleQuotesData(object):
	def __init__(self, symbols=None,date=None):
		self.date=date
		self.endTs=Helper().convertHumanTimeToUnixTimeStamp(date=self.date,time='17:00:00')
		self.symbols=symbols
		self.objQuotes=PolygonQuotesData()
		
	def getQuotesData(self):
		# Create URLs
		quotesRoutines=self.objQuotes.createQuotesUrlsForStocks(symbols=self.symbols, date=self.date, endTs= self.endTs)
		# Fetch Data for URLs
		finalResultDf=self.objQuotes.fetchQuotesDataFromPolygonAPI(quotesRoutines=quotesRoutines, date=self.date)
		# Save the finalResultDf into MongoDb one by one for each symbol
		for symbol in self.symbols:
			data=finalResultDf[finalResultDf['Symbol']==symbol]
			_ = self.objQuotes.saveQuotesDataInMongoDB(symbol=symbol, dateForQuotes=self.date, data=data)
		
if __name__ == "__main__":
	ob=AssembleQuotesData(symbols=['XLK'],date='2020-03-13')
	ob.getQuotesData()

