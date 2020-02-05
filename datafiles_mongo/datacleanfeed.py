import pandas as pd
import itertools
import time
import csv
import os
from datetime import datetime


class Details:
    def __init__(self, title, inception_date, fundholdings_date, totalassetsundermgmt, sharesoutstanding, expenseRatio,
                 indextracker, etfdb_category, issuer, structure, etf_homepage, holdings):
        self.title = title
        self.inception_date = inception_date
        self.fundHoldings_date = fundholdings_date
        self.totalAssetsUnderMgmt = totalassetsundermgmt
        self.sharesOutstanding = sharesoutstanding
        self.expenseRatio = expenseRatio
        self.indexTracker = indextracker
        self.etfdb_category = etfdb_category
        self.issuer = issuer
        self.structure = structure
        self.etf_homepage = etf_homepage

        self.Holdings = holdings


class PullandCleanData:
    def __init__(self):
        self.savingpath = '/home/piyush/Desktop/ETFApp_withMongo/ETFAnalysis/ETFDailyData' + '/' + datetime.now().strftime(
            "%Y%m%d")
        self.detailsdata = pd.DataFrame()
        self.holdingsdata = pd.DataFrame()

    def readfilesandclean(self):
        for filename in os.listdir(self.savingpath):
            self.detailsdata = pd.read_csv(self.savingpath + '/' + filename, sep='\:\s', nrows=11, index_col=False,
                                           names=['Key', 'Value'])
            self.detailsdata.iloc[5]['Value']=float(self.detailsdata.iloc[5]['Value'][:-1])

            print(self.detailsdata)



            self.holdingsdata = pd.read_csv(self.savingpath + '/' + filename, header=12,
                                            names=['Holdings', 'Symbol', 'Weights'])
            self.holdingsdata['Weights'] = list(map(lambda x: x[:-1], self.holdingsdata['Weights'].values))
            self.holdingsdata['Weights'] = [float(x) for x in self.holdingsdata['Weights'].values]
            print(self.holdingsdata)

pc = PullandCleanData()
pc.readfilesandclean()
