from pymongo import MongoClient
import pandas as pd
import datetime
import time
import numpy as np
import talib


from FlaskAPI.Components.ETFArbitrage.helperForETFArbitrage import LoadETFPrices, LoadETFArbitrageData, analysePerformance
from FlaskAPI.Components.ETFArbitrage.MomentumSignal import MomentumSignals
from FlaskAPI.Components.ETFArbitrage.CandleStickPattern import PatternSignals

connectionLocal = MongoClient('18.213.229.80', 27017)
db = connectionLocal.ETF_db
TradesData = db.TradesData
arbitragecollection = db.ArbitrageCollection



MomentumsignalsColumns = ['ADX Trend','AROONOSC Trend','Momentum Indicator','CMO Indicator',
						'RSI Indicator','ULTOC Indicator','Stochastic Indicator','WILLR Indicator','MFI Indicator']

CandlesignalsColumns = ['Hammer Pat','InvertedHammer Pat','DragonFlyDoji Pat','PiercingLine Pat','MorningStar Pat','MorningStarDoji Pat','3WhiteSoldiers Pat',
						'HanginMan Pat','Shooting Pat','GraveStone Pat','DarkCloud Pat','EveningStar Pat','EveningDoji Pat','3BlackCrows Pat','AbandonedBaby Pat',
						'Engulfing Pat','Harami Pat','IndecisionSpinningTop Pat','IndecisionDoji Pat','3LineStrike Pat']

MajorUnderlyingMovers=['ETFMover%1','ETFMover%2', 'ETFMover%3', 'ETFMover%4', 'ETFMover%5', 'ETFMover%6','ETFMover%7', 'ETFMover%8', 'ETFMover%9', 'ETFMover%10', 
						'Change%1','Change%2', 'Change%3', 'Change%4', 'Change%5', 'Change%6', 'Change%7','Change%8', 'Change%9', 'Change%10']


def AnalyzeArbitrageDataForETF(arbitrageDataFromMongo=None, magnitudeOfArbitrageToFilterOn=0):
	
	arbitrageBuySellSignals = pd.DataFrame()
	pricedf = pd.DataFrame()
	
	dateOfAnalysis=arbitrageDataFromMongo['dateOfAnalysis']
	year=dateOfAnalysis.year
	# Load Prices Data
	pricedf=LoadETFPrices(arbitrageDataFromMongo['ETFName'],dateOfAnalysis,year,TradesData)
	# Load Arbitrage Data
	etfdata=LoadETFArbitrageData(arbitrageDataFromMongo['data'],dateOfAnalysis,year)

	df=pd.merge(etfdata,pricedf,on='Time',how='left')
	df=df.ffill(axis=0)

	df['Magnitude of Arbitrage']=abs(df['ETF Trading Spread in $']-abs(df['Arbitrage in $']))
	df['Flag'] = 0
	a = (abs(df['Arbitrage in $']) > df['ETF Trading Spread in $'])
	b = df['ETF Trading Spread in $'] != 0
	c = df['Magnitude of Arbitrage'] > magnitudeOfArbitrageToFilterOn
	df.loc[a & b & c, 'Flag'] = 111
	df['Flag'] = df['Flag'] * np.sign(df['Arbitrage in $'])
	df=df.set_index('Time')

	# Build Signals
	df=MomentumSignals(df,tp=10)
	df=PatternSignals(df)

	columnsneeded=['ETF Trading Spread in $','Arbitrage in $','Magnitude of Arbitrage','Flag']
	#columnsneeded=columnsneeded+MomentumsignalsColumns+CandlesignalsColumns+MajorUnderlyingMovers
	columnsneeded=columnsneeded+MajorUnderlyingMovers

	etfOverBought = df.loc[df['Flag']== 111.0]
	PNLSellPositionsT_1=0
	if etfOverBought.shape[0]!=0:
		sellPositions = analysePerformance(df=df, BuySellIndex=etfOverBought)
		tempdf=df.loc[etfOverBought.index]
		tempdf=tempdf[columnsneeded]
		sellPositions=pd.merge(tempdf,sellPositions,how='outer',left_index=True,right_index=True)
		
		'''
		print("Date ="+str(dateOfAnalysis))
		print("Sell Positions Probability")
		print(sellPositions[sellPositions<0].count()/sellPositions.shape[0])
		print("Sell Positions N+1 Days")
		print(sellPositions)
		'''

		# Drop the last row
		sellPositions.drop(sellPositions.tail(1).index,inplace=True)
		arbitrageBuySellSignals = arbitrageBuySellSignals.append(sellPositions)

		PNLSellPositionsT_1 =-(sellPositions['T+1'].sum())

	etfOverSold = df.loc[df['Flag']== -111.0]

	PNLBuyPositionsT_1=0
	if etfOverSold.shape[0]!=0:
		buyPositions  = analysePerformance(df=df, BuySellIndex=etfOverSold)
		tempdf=df.loc[etfOverSold.index]
		tempdf=tempdf[columnsneeded]
		buyPositions=pd.merge(tempdf,buyPositions,how='outer',left_index=True,right_index=True)

		'''
		print("Buy Positions Probability")
		print(buyPositions[buyPositions>0].count()/buyPositions.shape[0])
		print("Buy Positions N+1 Days")
		print(buyPositions)
		'''

		# Dropt the last row
		buyPositions.drop(buyPositions.tail(1).index,inplace=True)
		arbitrageBuySellSignals = arbitrageBuySellSignals.append(buyPositions)

		PNLBuyPositionsT_1 =buyPositions['T+1'].sum()

	scatterPlotData=df[['ETF Change Price %','Net Asset Value Change%']].to_dict(orient='records')
	pnlstatementforday = {'PNL% Sell Pos. (T+1)':PNLSellPositionsT_1,
							   'PNL% Buy Pos. (T+1)':PNLBuyPositionsT_1}
	
	return arbitrageBuySellSignals, pricedf, pnlstatementforday, scatterPlotData


# Historical arbitrage data for just 1 etf for 1 date
def RetrieveETFArbitrageData(etfname=None, date=None, magnitudeOfArbitrageToFilterOn=0):
	print(etfname)
	print(date)
	s=arbitragecollection.find({'ETFName':etfname,'dateOfAnalysis':datetime.datetime.strptime(date,'%Y%m%d')})
	
	# Iter over the collection results - It's just 1 item
	PNLStatementForTheDay={}
	for i in s:
		allData, pricedf, pnlstatementforday, scatterPlotData=AnalyzeArbitrageDataForETF(arbitrageDataFromMongo=i, magnitudeOfArbitrageToFilterOn=magnitudeOfArbitrageToFilterOn)
		PNLStatementForTheDay[str(i['dateOfAnalysis'])]=pnlstatementforday
	print(PNLStatementForTheDay)
	return allData, pricedf, PNLStatementForTheDay, scatterPlotData


# This function sends back PNL for all dates for ETF 
def retrievePNLForAllDays(etfname=None, magnitudeOfArbitrageToFilterOn=0):
	s=arbitragecollection.find({'ETFName':etfname})
	PNLOverDates={}
	# Iter over the collection results
	for i in s:
		allData, pricedf, pnlstatementforday, scatterPlotData=AnalyzeArbitrageDataForETF(arbitrageDataFromMongo=i, magnitudeOfArbitrageToFilterOn=magnitudeOfArbitrageToFilterOn)
		PNLOverDates[str(i['dateOfAnalysis'])]=pnlstatementforday

	print(PNLOverDates)
	return PNLOverDates



























