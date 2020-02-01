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


###### Do the Arbitrage analysis work
class ETFArbitrage(object):

    def __init__(self,etfob,weightedStockReturns):
        self.navDF=pd.merge(etfob,weightedStockReturns['NAV'],left_index=True,right_index=True)
        self.navDF['Date']=self.navDF.index
        self.navDF['Close']=self.navDF['Close']*100
        self.navDF['NAV']=self.navDF['NAV']*100
        del self.navDF['Date']
        self.navDF['Mispricing']=(self.navDF['Close']-self.navDF['NAV'])
        

class CleanDataForJinga(object):

    def __init__(self,data,columnRearrange,indexColumnName):
        self.data=data
        self.columnRearrange=columnRearrange
        self.indexColumnName=indexColumnName

    def CleanForEndUser(self):
        self.data[self.indexColumnName]=self.data.index
        self.data=self.data[self.columnRearrange]
        self.data=self.data.reset_index(drop=True)

        # Normalize Dates from '2020-01-01 00:00:00' to '2020-01-01' in pandas
        if indexColumnName=='Date':
            self.data.index = self.data.index.normalize()

        return self.data

class ZscoreAnanlysisByAttribute():

    def __init__(self,data,zthresh,colname):
        self.data=data
        self.data.name=self.data.name+' '+colname
        self.zthresh=zthresh
        
    def getMispricedData(self):
        self.df=self.data.to_frame()
        self.df['Z-Score']=np.abs(stats.zscore(self.df.values.tolist()))
        self.requiredDF=self.df[self.df['Z-Score']>self.zthresh]
        return self.requiredDF









    