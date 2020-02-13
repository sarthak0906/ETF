import pandas as pd
import itertools
import time
import csv
import os
from datetime import datetime
from mongoengine import *

from MongoDB.List523ETFsMongo import ETFListDocument
from MongoDB.ETFListCollection import ETFListData

from MongoDB.ETFMongo import ETF
from MongoDB.HoldingsMongo import Holdings

connect('ETF_db', alias='ETF_db')


class ETFDetails(object):

    def __init__(self):
        self.todaysdata = ETFListDocument.objects(Download_date=datetime.now().date()).first()
        self.etfdescdf = pd.DataFrame(self.todaysdata.to_mongo().to_dict()['etflist'])

    def ReturnetfDF(self):
        return self.etfdescdf


class PullandCleanData:
    def __init__(self):
        self.savingpath = '../ETFDailyData' + '/' + datetime.now().strftime("%Y%m%d")
        self.detailsdata = pd.DataFrame()
        self.holdingsdata = pd.DataFrame()
        self.etfdescdf = ETFDetails().ReturnetfDF()

    def readfilesandclean(self):
        # details = Details()
        for filename in os.listdir(self.savingpath):
            try:
                if filename not in ['.DS_Store', 'IXG-holdings.csv']:
                    etfticker = filename.split('-')[0]
                    print("Data loaded to Db=" + etfticker)
                    self.detailsdata = pd.read_csv(self.savingpath + '/' + filename, sep='\:\s', nrows=11,
                                                   index_col=False,
                                                   names=['Key', 'Value'])

                    self.detailsdata.iloc[5]['Value'] = float(self.detailsdata.iloc[5]['Value'][:-1])
                    # Check for NaN Values in IndexTracker, if it exsists replace with None

                    self.holdingsdata = pd.read_csv(self.savingpath + '/' + filename, header=12,
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
                        ETFName=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['ETFName'].values[0]),
                        AverageVolume=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['AverageVolume'].values[0]),
                        Leveraged=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['Leveraged'].values[0]),
                        Inversed=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['Inversed'].values[0]),
                        CommissionFree=str(
                            self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['CommissionFree'].values[0]),
                        AnnualDividendRate=str(
                            self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['AnnualDividendRate'].values[0]),
                        DividendDate=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['DividendDate'].values[0]),
                        Dividend=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['Dividend'].values[0]),
                        AnnualDividendYield=str(
                            self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['AnnualDividendYield'].values[0]),
                        PERatio=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['PERatio'].values[0]),
                        Beta=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['Beta'].values[0]),
                        NumberOfHolding=float(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['NumberOfHolding'].values[0]),
                        OverAllRating=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['OverAllRating'].values[0]),
                        LiquidityRating=str(
                            self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['LiquidityRating'].values[0]),
                        ExpensesRating=str(
                            self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['ExpensesRating'].values[0]),
                        ReturnsRating=str(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['ReturnsRating'].values[0]),
                        VolatilityRating=str(
                            self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['VolatilityRating'].values[0]),
                        DividendRating=str(
                            self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['DividendRating'].values[0]),
                        ConcentrationRating=str(
                            self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['ConcentrationRating'].values[0]),
                        ESGScore=float(self.etfdescdf.loc[self.etfdescdf['Symbol'] == etfticker]['ESGScore'].values[0]),
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
