#Gathers Data from APIs
# 1) Trade Data
# 2) Quotes Data
# 3) Daily/Open Close Data
# 4) ETFDB Data
import sys
sys.path.append("..")  # Remove in production - KTZ


import pandas as pd

from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
# Import Collections
from MongoDB.Schemas import quotesCollection, tradeCollection, dailyopencloseCollection
# Import Pipeline
from MongoDB.Schemas import quotespipeline, tradespipeline

from PolygonTickData.DataDailyOpenClose import DailyOpenCloseData
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata



class DataApi(object):

	def __init__(self, etfname=None, date=None):
		self.etfname=etfname
		self.date=date

		# Obejct for ETFdata
		self.etfData=self.gatherETFdbData()
		# Object for Trade Data
		self.tradesDataDf=self.gatherTradeData()
		# Object for Quotes Data
		self.quotesDataDf=self.gatherQuotesData()
		# Object for Open Close Data
		self.openPriceData=self.gatherOpenCloseData()

	def gatherETFdbData(self):
		return LoadHoldingsdata(etfname=self.etfname, fundholdingsdate=self.date)

	def gatherTradeData(self):
		ob = AssembleData(symbols=self.etfData.getSymbols(), date=self.date)
		tradesDataDf = ob.getData(CollectionName=tradeCollection,pipeline=tradespipeline, tradeDataFlag=True)
    
		return tradesDataDf    

	def gatherQuotesData(self):
		ob = AssembleData(symbols=[self.etfname], date=self.date)
		quotesDataDf = ob.getData(CollectionName=quotesCollection,pipeline=quotespipeline)
		return quotesDataDf
		
	def gatherOpenCloseData(self):
		return DailyOpenCloseData(symbols=self.etfData.getSymbols(), date=self.date, collectionName=dailyopencloseCollection).run()


if __name__ == "__main__":
	ob=DataApi(etfname='XLK', date='2020-03-16')
	print(ob.etfData)
	print(ob.tradesDataDf)
	print(ob.quotesDataDf)
	print(ob.openPriceData)











