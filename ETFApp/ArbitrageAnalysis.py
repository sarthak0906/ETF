import pandas as pd
import numpy as np
from scipy import stats


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

	def findZScore(self,df=None,zthresh=None,colname=None):
		# Check if the object is not a pandas dataframe, if not convert it
		if isinstance(df,pd.Series):
			df=df.to_frame()
			df.columns=[colname]
		df['Z-Score']=np.abs(stats.zscore(df[colname].tolist()))
		requiredDF=df[df['Z-Score']>zthresh]
		return requiredDF


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
		kvpairs={}

		tempOb=StatisticalCalculations()
		daysofarbitrage=tempOb.findZScore(df=daysofarbitrage,zthresh=stdthresold,colname='Mispricing')
		
		for ticker in tickers:
			weightedMovement=changeDF[ticker]*constituentdata['Volume'][ticker]
			weightedMovement=weightedMovement.dropna()

			tempOb=StatisticalCalculations()
			stockVolumeStd=tempOb.findZScore(df=constituentdata['Volume'][ticker],zthresh=stdthresold,colname='Volume')
			stockReturnStd=tempOb.findZScore(df=changeDF[ticker]*100,zthresh=stdthresold,colname='Return')
			stockweightedmovement=tempOb.findZScore(df=weightedMovement,zthresh=stdthresold,colname='Volume Weighted Return')
			
			d=[list(daysofarbitrage.index),list(stockweightedmovement.index)]

			# Get list of intersection dates betweeen daysofarbitrage & stockweightedmovement
			lst=(list(set.intersection(*map(set,d))))
			
			# Check if intersection didn't give 0
			if len(lst)>0:
				kvpairs[ticker]=lst

		MispriceDF=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in kvpairs.items() ]))
		print(MispriceDF.T)

		return self.NavDfwithKvPairs(kvpairs,daysofarbitrage)

	def NavDfwithKvPairs(self,kvpairs,daysofarbitrage):
		stockscausingmispricing=StatisticalCalculations().invertDict(kvpairs)
		daysofarbitrage['Stocks Responsible Mispricing'] = daysofarbitrage.index.to_series().map(stockscausingmispricing)
		return daysofarbitrage








	

