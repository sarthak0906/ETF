import pandas as pd
import itertools
import time
import csv
import os
from datetime import datetime
from mongoengine import *

from ETFMongo import ETF
from HoldingsMongo import Holdings

connect('ETF_db', alias='ETF_db')


class PullandCleanData():
    def __init__(self):
        self.savingpath = '../ETFDailyData' + '/' + datetime.now().strftime("%Y%m%d")
        self.detailsdata = pd.DataFrame()
        self.holdingsdata = pd.DataFrame()

    def readfilesandclean(self):
        # details = Details()
        for filename in os.listdir(self.savingpath):
          if filename not in ['.DS_Store','IXG-holdings.csv']:
            print("***************")
            print(filename)
            
            self.detailsdata = pd.read_csv(self.savingpath + '/' + filename, sep='\:\s', nrows=11, index_col=False,
                                           names=['Key', 'Value'])
            self.detailsdata.iloc[5]['Value'] = float(self.detailsdata.iloc[5]['Value'][:-1])
            
            # Check for NaN Values in IndexTracker, if it exsists replace with None
            
            if str(self.detailsdata.iloc[6]['Value'])=='nan':
              self.detailsdata.iloc[6]['Value']='None'

            self.holdingsdata = pd.read_csv(self.savingpath + '/' + filename, header=12,names=['Holdings', 'Symbol', 'Weights'])
            self.holdingsdata['Weights'] = list(map(lambda x: x[:-1], self.holdingsdata['Weights'].values))
            self.holdingsdata['Weights'] = [float(x) for x in self.holdingsdata['Weights'].values]

            print(self.detailsdata)
            print(self.holdingsdata)
            print("***************")

            details = ETF(title=self.detailsdata.iloc[0]['Key'],
                          inception_date=datetime.strptime(self.detailsdata.iloc[1]['Value'], '%Y-%m-%d'),
                          FundHoldings_date=datetime.strptime(self.detailsdata.iloc[2]['Value'], '%Y-%m-%d'),
                          TotalAssetsUnderMgmt=float(self.detailsdata.iloc[3]['Value']) * 1000,
                          SharesOutstanding=float(self.detailsdata.iloc[4]['Value']),
                          ExpenseRatio=float(self.detailsdata.iloc[5]['Value']),
                          IndexTracker=self.detailsdata.iloc[6]['Value'],
                          ETFdbCategory=self.detailsdata.iloc[7]['Value'],
                          Issuer=self.detailsdata.iloc[8]['Value'],
                          Structure=self.detailsdata.iloc[9]['Value'],
                          ETFhomepage=self.detailsdata.iloc[10]['Value'],
                          )
            for index, row in self.holdingsdata.iterrows():
                holding = Holdings()
                holding.TickerName = row.Holdings
                holding.TickerSymbol = row.Symbol
                holding.TickerWeight = row.Weights
                details.holdings.append(holding)
            details.save()

if __name__ == "__main__":
  PullandCleanData().readfilesandclean()
  
