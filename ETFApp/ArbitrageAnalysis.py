import pandas as pd
import numpy as np

class ZscoreAnlysByAttr():

    def __init__(self,data,zthresh,colname):
        self.data=data
        self.data.name=self.data.name+' '+colname
        self.zthresh=zthresh
        
    def FindZScore(self):
        self.df=self.data.to_frame()
        self.df['Z-Score']=np.abs(stats.zscore(self.df.values.tolist()))
        self.requiredDF=self.df[self.df['Z-Score']>self.zthresh]
        return self.requiredDF

class ArbitrageAnalysis(object):

	def __init__(self):
		pass

	def 

	

