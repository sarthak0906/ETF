import pandas as pd
import itertools
import time
import csv
import os
from datetime import datetime
from mongoengine import *

from ETFMongo import ETF
from HoldingsMongo import Holdings



class PullandCleanData:
    
    def __init__(self):
        self.savingpath = '../ETFDailyData' + '/' + datetime.now().strftime("%Y%m%d")
        self.detailsdata = pd.DataFrame()
        self.holdingsdata = pd.DataFrame()
        connect('ETF_db', alias='ETF_db')

    def readfilesandclean(self, etfname, etfdescdf):
        # details = Details()
        for file in os.listdir(self.savingpath):
            filename = file.split('-')[0]
            try:
                if filename == etfname and file not in ['.DS_Store']:
                    
                    print("Data loaded to Db=" + filename)
                    self.detailsdata = pd.read_csv(self.savingpath + '/' + file, sep='\:\s', nrows=11,
                                                   index_col=False,
                                                   names=['Key', 'Value'])

                    self.detailsdata.iloc[5]['Value'] = float(self.detailsdata.iloc[5]['Value'][:-1])
                    # Check for NaN Values in IndexTracker, if it exsists replace with None

                    self.holdingsdata = pd.read_csv(self.savingpath + '/' + file, header=12,
                                                    names=['Holdings', 'Symbol', 'Weights'])
                    self.holdingsdata['Weights'] = list(map(lambda x: x[:-1], self.holdingsdata['Weights'].values))
                    self.holdingsdata['Weights'] = [float(x) for x in self.holdingsdata['Weights'].values]

                    details = ETF(
                        ETFTicker=self.detailsdata.iloc[0]['Key'],
                        InceptionDate=datetime.strptime(self.detailsdata.iloc[1]['Value'], '%Y-%m-%d'),
                        FundHoldingsDate=datetime.strptime(self.detailsdata.iloc[2]['Value'], '%Y-%m-%d'),
                        TotalAssetsUnderMgmt=str(self.detailsdata.iloc[3]['Value']),
                        SharesOutstanding=str(self.detailsdata.iloc[4]['Value']),
                        ExpenseRatio=str(self.detailsdata.iloc[5]['Value']),
                        IndexTracker=str(self.detailsdata.iloc[6]['Value']),
                        ETFdbCategory=self.detailsdata.iloc[7]['Value'],
                        Issuer=self.detailsdata.iloc[8]['Value'],
                        Structure=self.detailsdata.iloc[9]['Value'],
                        ETFhomepage=self.detailsdata.iloc[10]['Value'],
                        ETFName=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['ETFName'].values[0]),
                        AverageVolume=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['AverageVolume'].values[0]),
                        Leveraged=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['Leveraged'].values[0]),
                        Inversed=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['Inversed'].values[0]),
                        CommissionFree=str(
                            etfdescdf.loc[etfdescdf['Symbol'] == etfname]['CommissionFree'].values[0]),
                        AnnualDividendRate=str(
                            etfdescdf.loc[etfdescdf['Symbol'] == etfname]['AnnualDividendRate'].values[0]),
                        DividendDate=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['DividendDate'].values[0]),
                        Dividend=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['Dividend'].values[0]),
                        AnnualDividendYield=str(
                            etfdescdf.loc[etfdescdf['Symbol'] == etfname]['AnnualDividendYield'].values[0]),
                        PERatio=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['PERatio'].values[0]),
                        Beta=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['Beta'].values[0]),
                        NumberOfHolding=float(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['NumberOfHolding'].values[0]),
                        OverAllRating=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['OverAllRating'].values[0]),
                        LiquidityRating=str(
                            etfdescdf.loc[etfdescdf['Symbol'] == etfname]['LiquidityRating'].values[0]),
                        ExpensesRating=str(
                            etfdescdf.loc[etfdescdf['Symbol'] == etfname]['ExpensesRating'].values[0]),
                        ReturnsRating=str(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['ReturnsRating'].values[0]),
                        VolatilityRating=str(
                            etfdescdf.loc[etfdescdf['Symbol'] == etfname]['VolatilityRating'].values[0]),
                        DividendRating=str(
                            etfdescdf.loc[etfdescdf['Symbol'] == etfname]['DividendRating'].values[0]),
                        ConcentrationRating=str(
                            etfdescdf.loc[etfdescdf['Symbol'] == etfname]['ConcentrationRating'].values[0]),
                        ESGScore=float(etfdescdf.loc[etfdescdf['Symbol'] == etfname]['ESGScore'].values[0]),
                    )

                    for index, row in self.holdingsdata.iterrows():
                        holding = Holdings()
                        holding.TickerName = row.Holdings
                        holding.TickerSymbol = row.Symbol
                        holding.TickerWeight = row.Weights
                        details.holdings.append(holding)
                    details.save()
            except Exception as e:
                print(e)
                continue
if __name__== "__main__":

    PullandCleanData().readfilesandclean()