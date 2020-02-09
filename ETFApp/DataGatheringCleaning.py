import datetime as dt
import pandas as pd
import pandas_datareader.data as web
from scipy import stats
import numpy as np
import time
from itertools import chain


##### ETF Data Clean up ###########
class ETFDataCleanup(object):
    
    def __init__(self):
        pass

    def showNaColumns(self,df):
        s=df.isnull().sum()
        print(s[s>0])
    
    def dropNAColumns(self,df):
        return df.dropna(axis='columns')
    
    def computeDailyReturns(self,df):
        return df.pct_change().dropna()        
    
    
####### Get Data for Constituents of ETF
class ConstituentsData(ETFDataCleanup):
    
    def __init__(self):
        self.constituentdata=[]
        self.constituentcloseDF=[]
        self.tickerdf=[]
        self.changeDF=[]
        self.weightedStockReturns=[]
    
    def loadETFWeights(self,fileName):
        self.etfWeights = pd.read_excel(fileName)
        self.etfWeights.set_index('Ticker',inplace=True)

    def getStockPrices(self,startdate,enddate):
        tickers=self.etfWeights.index
        self.constituentdata =  web.DataReader(tickers,'yahoo',startdate,enddate)
        self.constituentcloseDF = self.constituentdata['Close'].iloc[:, :]
        
    def stringWeightsToFloat(self):
        self.etfWeights['Weights']=self.etfWeights['Weights'].apply(lambda x: x.replace('%','')).astype(float)
    
    def findNetAssetValue(self):
        self.weightedStockReturns=self.changeDF.copy()
        for col in self.changeDF.columns:
            # Divide by 100 for weights percentage eg 23.28%
            self.weightedStockReturns[col]=self.changeDF[col]*self.etfWeights['Weights'].loc[col]/100
        self.weightedStockReturns['NAV']=self.weightedStockReturns.sum(axis=1)

####### Get prices of ETF        
class ETFStockPrices(ETFDataCleanup):
    
    def __init__(self,etfticker=None):
        self.etfticker=etfticker
        self.etfdata=[]
        self.etfchangeDF=[]

    def getETFTickerData(self,startdate,enddate):
        self.etfdata =  web.DataReader(self.etfticker,'yahoo',startdate,enddate)




