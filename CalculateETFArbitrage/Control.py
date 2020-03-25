import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
import logging

from PolygonTickData.Helper import Helper
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
from CalculateETFArbitrage.GatherData import DataApi

# Create an object of ETF Hoding Data
etfname = 'SCHH'
date = '2020-03-16'

# Load the ETF Holding
etfData = LoadHoldingsdata(etfname=etfname, fundholdingsdate=date)

# Load all the data - Holdings data for Etf, trade data, quotes data, open-close price
allData = DataApi(etfname=etfname, date=date, etfData=etfData) 

print(allData.tradesDataDf)
print(allData.quotesDataDf)

# Convert Time Stamps to Pandas Timestamp
helperObj = Helper()
allData.tradesDataDf['Time'] = allData.tradesDataDf['Time'].apply(lambda x: helperObj.getHumanTime(ts=x, divideby=1000))
tradePricesDFMinutes = allData.tradesDataDf.groupby([allData.tradesDataDf['Time'],allData.tradesDataDf['Symbol']])['Trade Price']
tradePricesDFMinutes=tradePricesDFMinutes.first().unstack(level=1)
tradePricesDFMinutes.to_csv("MinutesData.csv")


tradePricesDFMinutes = tradePricesDFMinutes.fillna(method='ffill')
priceforNAVfilling = allData.openPriceData.to_dict()
tradePricesDFMinutes = tradePricesDFMinutes.fillna(priceforNAVfilling)


allData.quotesDataDf['Time'] = allData.quotesDataDf['Time'].apply(lambda x: helperObj.getHumanTime(ts=x, divideby=1000000000))
allData.quotesDataDf = allData.quotesDataDf[allData.quotesDataDf['Bid Size'] != 0]
allData.quotesDataDf = allData.quotesDataDf[allData.quotesDataDf['Ask Size'] != 0]
allData.quotesData['Spread'] = allData.quotesData['Ask Price'] - allData.quotesData['Bid Price']
allData.quotesData['MidPrice'] = (allData.quotesData['Ask Price'] + allData.quotesData['Bid Price']) / 2



print(allData.tradesDataDf)
print(allData.quotesDataDf)
print(allData.openPriceData.to_dict())
print(tradePricesDFMinutes)


