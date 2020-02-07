import pandas as pd
import numpy as np
from scipy import stats
from functools import reduce


###### Do the Arbitrage analysis work
class ETFArbitrage(object):

	def __init__(self,etfob,weightedStockReturns):
		self.navDF=pd.merge(etfob,weightedStockReturns['NAV'],left_index=True,right_index=True)
		self.navDF['Date']=self.navDF.index
		self.navDF['Close']=self.navDF['Close']*100
		self.navDF['NAV']=self.navDF['NAV']*100
		del self.navDF['Date']
		self.navDF['Mispricing']=(self.navDF['Close']-self.navDF['NAV'])


class StatisticalCalculations():

	def __init__(self):
		pass

	def findZScore(self,df=None,colname=None):
		# Check if the object is not a pandas dataframe, if not convert it
		if isinstance(df,pd.Series):
			df=df.to_frame()
			df.columns=[colname]
		df[colname+' Z-Score']=stats.zscore(df[colname].tolist()).round(2)
		return df

	def getDataAboveThresold(self,df,zthresh=None):
		df=df[df[colname+' Z-Score']>zthresh]
		return df

	def invertDict(self,d):
		newdict = {}
		for key, value in d.items():
			for string in value:
				newdict.setdefault(string, []).append(key)
		return newdict

class ArbitrageAnalysis(object):

	def __init__(self):
		pass
		
	def GetArbDataFrame(self,tickers=None,constituentdata=None,changeDF=None,daysofarbitrage=None,stdthresold=None):
		# Making Sure that Both ChangeDF and constituentdata has same Number of Dates, Since we dropped NA in change -KTZ
		tickersSTDdata={}
		statOb=StatisticalCalculations()
		daysofarbitrage=statOb.findZScore(df=daysofarbitrage,colname='Mispricing')
		
		for ticker in tickers:
			tickersSTDdata[ticker]=self.getConstituentsStdData(ticker,changeDF,constituentdata,statOb)
		
		print(tickersSTDdata)
		print(daysofarbitrage)
		return daysofarbitrage, tickersSTDdata

	def getConstituentsStdData(self,ticker,changeDF,constituentdata,statOb):
		weightedMovement=changeDF[ticker]*constituentdata['Volume'][ticker]
		weightedMovement=weightedMovement.dropna()

		stockVolumeStd=statOb.findZScore(df=constituentdata['Volume'][ticker],colname='Vol.')
		stockReturnStd=statOb.findZScore(df=changeDF[ticker]*100,colname='Return')
		stockweightedmovement=statOb.findZScore(df=weightedMovement,colname='Vol. Wgt Return')
		df=[stockVolumeStd,stockReturnStd,stockweightedmovement]
		df_merged = reduce(lambda  left,right: pd.merge(left,right,left_index=True,right_index=True,how='outer'), df)
		return df_merged[['Vol. Z-Score','Return Z-Score','Vol. Wgt Return Z-Score']].dropna()


	def getZScoresOnDate(self,date,tickersSTDdata):
		ZScoresOnDate={}
		for key,value in tickersSTDdata.items():
			ZScoresOnDate[key]=dict(value.loc[date])
		return pd.DataFrame.from_dict(ZScoresOnDate).T





	

