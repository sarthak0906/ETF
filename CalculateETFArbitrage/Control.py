import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
import logging
from functools import reduce

from PolygonTickData.Helper import Helper
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
from CalculateETFArbitrage.GatherData import DataApi

# Create an object of ETF Hoding Data
etfname = 'IHI'
date = '2020-03-16'

# Load the ETF Holding
etfData = LoadHoldingsdata(etfname=etfname, fundholdingsdate=date)

# Load all the data - Holdings data for Etf, trade data, quotes data, open-close price
allData = DataApi(etfname=etfname, date=date, etfData=etfData) 

# Convert Time Stamps to Pandas Timestamp
helperObj = Helper()
allData.tradesDataDf['Time'] = allData.tradesDataDf['Time'].apply(lambda x: helperObj.getHumanTime(ts=x, divideby=1000))
tradePricesDFMinutes = allData.tradesDataDf.groupby([allData.tradesDataDf['Time'],allData.tradesDataDf['Symbol']])['Trade Price']
tradePricesDFMinutes=tradePricesDFMinutes.first().unstack(level=1)
priceforNAVfilling = allData.openPriceData.set_index('Symbol').T.to_dict('records')[0]
tradePricesDFMinutes = tradePricesDFMinutes.fillna(priceforNAVfilling)

etfprice = tradePricesDFMinutes[etfname]
tradePricesDFMinutes = tradePricesDFMinutes.pct_change().dropna() * 100

etfpricechange = tradePricesDFMinutes[etfname]
del tradePricesDFMinutes[etfname]


allData.quotesDataDf['Time'] = allData.quotesDataDf['Time'].apply(lambda x: helperObj.getHumanTime(ts=x, divideby=1000000000))
allData.quotesDataDf = allData.quotesDataDf[allData.quotesDataDf['Bid Size'] != 0]
allData.quotesDataDf = allData.quotesDataDf[allData.quotesDataDf['Ask Size'] != 0]
allData.quotesDataDf['Total Bid Ask Size'] = allData.quotesDataDf['Ask Size'] + allData.quotesDataDf['Bid Size']
allData.quotesDataDf['Spread'] = allData.quotesDataDf['Ask Price'] - allData.quotesDataDf['Bid Price']
allData.quotesDataDf['MidPrice'] = (allData.quotesDataDf['Ask Price'] + allData.quotesDataDf['Bid Price']) / 2
allData.quotesDataDf = allData.quotesDataDf.groupby([allData.quotesDataDf['Time'].dt.hour, allData.quotesDataDf['Time'].dt.minute],group_keys=False).apply(helperObj.vwap)
allData.quotesDataDf['Time'] = allData.quotesDataDf['Time'].map(lambda x: x.replace(second=0))
quotesSpreadsMinutes = allData.quotesDataDf.groupby('Time')['vwap'].mean()

netassetvaluereturn = tradePricesDFMinutes.assign(**etfData.getETFWeights()).mul(tradePricesDFMinutes).sum(axis=1)

ds=pd.concat([etfprice, etfpricechange, netassetvaluereturn, quotesSpreadsMinutes], axis=1).dropna()
ds.columns = ['ETF Price', 'ETF Change Price %', 'Net Asset Value Change%', 'ETF Trading Spread in $']
ds['Arbitrage in $'] = (ds['ETF Change Price %'] - ds['Net Asset Value Change%']) * ds['ETF Price'] / 100
ds['Arbitrage in $'] = abs(ds['Arbitrage in $'])
ds['Flag'] = 0
ds.loc[(ds['Arbitrage in $'] > ds['ETF Trading Spread in $']) & ds['ETF Trading Spread in $'] != 0, 'Flag'] = 111
print(ds)

'''
tradePricesDFMinutes.to_csv("TradePrices.csv")
quotesSpreadsMinutes.to_csv("QuotesPrices.csv")
quotesSpreadsMinutes.to_csv("QuotesPrices2.csv")
quotesSpreadsMinutes = allData.quotesDataDf.groupby([allData.quotesDataDf['Time'].dt.hour, allData.quotesDataDf['Time'].dt.minute])['Spread'].mean()
quotesSpreadsMinutes = quotesSpreadsMinutes.unstack(level=1)
'''        




