import sys
sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from CommonServices.ThreadingRequests import IOBoundThreading
from MongoDB.CommonTradeQuotes import MongoDailyOpenCloseData

class DailyOpenCloseData(object):

	def __init__(self,symbols=None, date=None, collectionName=None):
		self.symbols=symbols
		self.date=date
		self.collectionName=collectionName
		self.dailyopencloseObj = MongoDailyOpenCloseData()

	def createUrls(self, symbolsToBeDownloaded=None):
		return [PolgonDataCreateURLS().PolygonDailyOpenClose(date=self.date, symbol=symbol) for symbol in symbolsToBeDownloaded]

	# Used for threading
	def getSaveOpenCloseData(self,openCloseURLs=None):
		responses=IOBoundThreading(openCloseURLs)
		priceforNAVfilling={}
		for response in responses:
			print(response)
			del response['status']
			del response['from']
			self.dailyopencloseObj.insertIntoCollection(symbol=response['symbol'], datetosave=self.date, savedata=response, CollectionName=self.collectionName)
	
	def fetchData(self):
		return self.dailyopencloseObj.fetchDailyOpenCloseData(symbolList=self.symbols, date=self.date, CollectionName=self.collectionName)

	# Check if symbol,date pair exist in MongoDB, If don't exist download URLs for the symbols
	def checkIfDataExsistInMongoDB(self, symbols=None, date=None, CollectionName=None):
		symbolsToBeDownloaded = []
		for symbol in symbols:
			if not self.dailyopencloseObj.doesItemExsistInQuotesTradesMongoDb(symbol, date, CollectionName):
				symbolsToBeDownloaded.append(symbol)
		return symbolsToBeDownloaded

	def run(self):
		symbolsToBeDownloaded = self.checkIfDataExsistInMongoDB(symbols=self.symbols, date=self.date, CollectionName=self.collectionName)

		if len(symbolsToBeDownloaded)>0:
			# Create New URLS
			createNewUrls=self.createUrls(symbolsToBeDownloaded=symbolsToBeDownloaded)
			# Save data for those URls
			_ = self.getSaveOpenCloseData(openCloseURLs=createNewUrls)

		data=self.fetchData()
		return pd.DataFrame(data)
'''
# Debugger Code
	# TO debug where it's failling
	def debuggetOpenCloseData(self,openCloseURLs=None):
		import urllib.request
		import json
		priceforNAVfilling={}
		for url in openCloseURLs:
			print(url)
			response=json.loads(urllib.request.urlopen(url).read())
			print(response)
			priceforNAVfilling[response['symbol']] = response['open']
		return priceforNAVfilling

if __name__=="__main__":
	from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
	from MongoDB.Schemas import dailyopencloseCollection
	etfData=LoadHoldingsdata(etfname='XLK', fundholdingsdate='2020-03-16')
	data=DailyOpenCloseData(symbols=etfData.getSymbols(), date='2020-03-16',collectionName=dailyopencloseCollection).run()
	print(data)
	#obj.debuggetOpenCloseData(openCloseURLs=obj.createUrls())
# Debugger Code
'''