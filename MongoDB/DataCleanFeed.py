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


class ETFDetails(object):
  
    def __init__(self):
        pathtoread="../ETFDailyData/ETFTIckersDecription/"+datetime.now().strftime("%Y%m%d")+"/etfs_details_type_fund_flow.csv"
        self.etfDesc=pd.read_csv(pathtoread)
        self.etfDesc.index=self.etfDesc['Symbol']
    
    def ReturnetfDict(self):
        return self.etfDesc.T.to_dict()

class PullandCleanData():
    def __init__(self):
        self.savingpath = '../ETFDailyData' + '/' + datetime.now().strftime("%Y%m%d")
        
        self.detailsdata = pd.DataFrame()
        self.holdingsdata = pd.DataFrame()
        self.etfDesc=ETFDetails().ReturnetfDict()

    def readfilesandclean(self):
        # details = Details()
        for filename in os.listdir(self.savingpath):
          if filename not in ['.DS_Store','IXG-holdings.csv']:
            etfticker=filename.split('-')[0]
            print("Data loaded to Db="+etfticker)
            self.detailsdata = pd.read_csv(self.savingpath + '/' + filename, sep='\:\s', nrows=11, index_col=False,
                                           names=['Key', 'Value'])
            self.detailsdata.iloc[5]['Value'] = float(self.detailsdata.iloc[5]['Value'][:-1])
            
            # Check for NaN Values in IndexTracker, if it exsists replace with None
            
            self.holdingsdata = pd.read_csv(self.savingpath + '/' + filename, header=12,names=['Holdings', 'Symbol', 'Weights'])
            self.holdingsdata['Weights'] = list(map(lambda x: x[:-1], self.holdingsdata['Weights'].values))
            self.holdingsdata['Weights'] = [float(x) for x in self.holdingsdata['Weights'].values]

            
            details = ETF(title=self.detailsdata.iloc[0]['Key'],
                          inception_date=datetime.strptime(self.detailsdata.iloc[1]['Value'], '%Y-%m-%d'),
                          FundHoldings_date=datetime.strptime(self.detailsdata.iloc[2]['Value'], '%Y-%m-%d'),
                          TotalAssetsUnderMgmt=float(self.detailsdata.iloc[3]['Value']) * 1000,
                          SharesOutstanding=float(self.detailsdata.iloc[4]['Value']),
                          ExpenseRatio=float(self.detailsdata.iloc[5]['Value']),
                          IndexTracker=str(self.detailsdata.iloc[6]['Value']),
                          ETFdbCategory=self.detailsdata.iloc[7]['Value'],
                          Issuer=self.detailsdata.iloc[8]['Value'],
                          Structure=self.detailsdata.iloc[9]['Value'],
                          
                          # New Data For DB
                          AverageVolume=str(self.etfDesc[etfticker]['Avg Volume']),
                          Leveraged=str(self.etfDesc[etfticker]['Leveraged']),
                          Inversed=str(self.etfDesc[etfticker]['Inverse']),
                          CommissionFree=str(self.etfDesc[etfticker]['Commission Free']),
                          AnnualDividendRate=str(self.etfDesc[etfticker]['Annual Dividend Rate']),
                          DividendDate=str(self.etfDesc[etfticker]['Dividend Date']),
                          Dividend=str(self.etfDesc[etfticker]['Dividend']),
                          AnnualDividendYield=str(self.etfDesc[etfticker]['Annual Dividend Yield %']),
                          PERatio=str(self.etfDesc[etfticker]['P/E Ratio']),
                          Beta=str(self.etfDesc[etfticker]['Beta']),
                          NumberOfHolding=str(self.etfDesc[etfticker]['# of Holdings']),
                          OverAllRating=str(self.etfDesc[etfticker]['Overall Rating']),
                          LiquidityRating=str(self.etfDesc[etfticker]['Liquidity Rating']),
                          ExpensesRating=str(self.etfDesc[etfticker]['Expenses Rating']),
                          ReturnsRating=str(self.etfDesc[etfticker]['Returns Rating']),
                          VolatilityRating=str(self.etfDesc[etfticker]['Volatility Rating']),
                          DividendRating=str(self.etfDesc[etfticker]['Dividend Rating']),
                          ConcentrationRating=str(self.etfDesc[etfticker]['Concentration Rating']),
                          ESGScore=str(self.etfDesc[etfticker]['ESG Score']),

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
  
