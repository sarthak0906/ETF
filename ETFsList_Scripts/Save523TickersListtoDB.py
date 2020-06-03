import pandas as pd
from datetime import datetime
from mongoengine import *

from ETFsList_Scripts.ETFListCollection import ETFListData
from ETFsList_Scripts.List523ETFsMongo import ETFListDocument


class ETFListSaver:

    def __init__(self):
        try:
            with open("MongoDBAccInfo.txt") as f:
                credentials = [x.strip().split(':', 1) for x in f]
            username = credentials[0][0]
            password = credentials[0][1]
        except :
            username = None
            password = None
            pass
        # connect to 'ETF_db' database in Mongodb with replica set
        if username is not None and password is not None:
            connect('ETF_db', alias='ETF_db', replicaSet='rs0', username=username, password=password)
        else:
            # READ ONLY ACCESS
            connect('ETF_db', alias='ETF_db', replicaSet='rs0', username='usertesterReadOnly', password='onlyreadpass')

        # connect to 'ETF_db' database in Mongodb without replica set
        # if username is not None and password is not None:
        #     connect('ETF_db', alias='ETF_db', username=username, password=password)
        # else:
        #     connect('ETF_db', alias='ETF_db', username='usertesterReadOnly', password='onlyreadpass')

        self.readingpath = ''
        self.etflistdf = pd.DataFrame()

    def readandclean(self):
        # specify path from where 523 etf list csv file is to be read
        self.readingpath = './ETFDailyData/ETFTickersDescription/' + datetime.now().strftime(
            "%Y%m%d") + '/etfs_details_type_fund_flow.csv'
        # read csv file into dataframe
        self.etflistdf = pd.read_csv(self.readingpath)
        print(self.etflistdf)

    def pushtodb(self):
        # Create document for db with 523 etf list
        etflistdocument = ETFListDocument(
            Download_date=datetime.now().date()
        )
        for index, row in self.etflistdf.iterrows():
            etflistdata = ETFListData()
            etflistdata.Symbol = str(row['Symbol'])
            etflistdata.ETFName = str(row['ETF Name'])
            etflistdata.AverageVolume = str(row['Avg. Daily Volume'])
            etflistdata.Leveraged = str(row['Leveraged'])
            etflistdata.Inversed = str(row['Inverse'])
            etflistdata.CommissionFree = str(row['Commission Free'])
            etflistdata.AnnualDividendRate = str(row['Annual Dividend Rate'])
            etflistdata.DividendDate = str(row['Dividend Date'])
            etflistdata.Dividend = str(row['Dividend'])
            etflistdata.AnnualDividendYield = str(row['Annual Dividend Yield %'])
            etflistdata.PERatio = str(row['P/E Ratio'])
            etflistdata.Beta = str(row['Beta'])
            etflistdata.NumberOfHolding = float(row['# of Holdings'])
            # etflistdata.OverAllRating = str(row['Overall Rating'])
            etflistdata.LiquidityRating = str(row['Liquidity Rating'])
            etflistdata.ExpensesRating = str(row['Expenses Rating'])
            etflistdata.ReturnsRating = str(row['Returns Rating'])
            etflistdata.VolatilityRating = str(row['Volatility Rating'])
            etflistdata.DividendRating = str(row['Dividend Rating'])
            etflistdata.ConcentrationRating = str(row['Concentration Rating'])
            etflistdata.ESGScore = float(row['ESG Score'])
            etflistdocument.etflist.append(etflistdata)
        # push to db
        etflistdocument.save()
        disconnect('ETF_db')