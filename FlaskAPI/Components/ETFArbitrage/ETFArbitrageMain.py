from pymongo import MongoClient
import pandas as pd
import datetime
import time
import numpy as np
import talib


from FlaskAPI.Components.ETFArbitrage.helperForETFArbitrage import LoadETFPrices, LoadETFArbitrageData, analysePerformance, countRightSignals
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


# 2 types of signals
# Signal Type 1 : When 111 = Sell and -111 = Buy
InverseSignal = ['FTEC']

# Signal Type 1 : When 111 = Buy and -111 = Sell
MaintainSignal = ['XLK','XLC','XLP']

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
	df['Over Bought/Sold'] = 0
	a = (abs(df['Arbitrage in $']) > df['ETF Trading Spread in $'])
	b = df['ETF Trading Spread in $'] != 0
	c = df['Magnitude of Arbitrage'] > magnitudeOfArbitrageToFilterOn
	df.loc[a & b & c, 'Over Bought/Sold'] = 111
	df['Over Bought/Sold'] = df['Over Bought/Sold'] * np.sign(df['Arbitrage in $'])
	df=df.set_index('Time')

	# Build Signals
	df=MomentumSignals(df,tp=10)
	df=PatternSignals(df)

	columnsneeded=['ETF Trading Spread in $','Arbitrage in $','Magnitude of Arbitrage','Over Bought/Sold']
	#columnsneeded=columnsneeded+MomentumsignalsColumns+CandlesignalsColumns+MajorUnderlyingMovers
	columnsneeded=columnsneeded+MajorUnderlyingMovers

	etfOverBought = df.loc[df['Over Bought/Sold']== 111.0]
	PNLSellPositionsT_1=0
	if etfOverBought.shape[0]!=0:
		sellPositions = analysePerformance(df=df, BuySellIndex=etfOverBought)
		tempdf=df.loc[etfOverBought.index]
		tempdf=tempdf[columnsneeded]
		sellPositions=pd.merge(tempdf,sellPositions,how='outer',left_index=True,right_index=True)
		# Drop the last row
		sellPositions.drop(sellPositions.tail(1).index,inplace=True)
		arbitrageBuySellSignals = arbitrageBuySellSignals.append(sellPositions)
		PNLSellPositionsT_1 =round(-(sellPositions['T+1'].sum()),2)
	etfOverSold = df.loc[df['Over Bought/Sold']== -111.0]

	PNLBuyPositionsT_1=0
	if etfOverSold.shape[0]!=0:
		buyPositions  = analysePerformance(df=df, BuySellIndex=etfOverSold)
		tempdf=df.loc[etfOverSold.index]
		tempdf=tempdf[columnsneeded]
		buyPositions=pd.merge(tempdf,buyPositions,how='outer',left_index=True,right_index=True)
		# Dropt the last row
		buyPositions.drop(buyPositions.tail(1).index,inplace=True)
		arbitrageBuySellSignals = arbitrageBuySellSignals.append(buyPositions)
		PNLBuyPositionsT_1 =round(buyPositions['T+1'].sum(),2)

	scatterPlotData=df[['ETF Change Price %','Net Asset Value Change%']].to_dict(orient='records')
	pricedf.columns=['date','volume','open','close','high','low']

	# Dvision By ETF Type
	# Some etfs have inverse signal, IF TRUE, than we stick with momentum and keep buying with it
	if arbitrageDataFromMongo['ETFName'] in MaintainSignal:
		pnlstatementforday = {'PNL% Sell Pos. (T+1)':-PNLBuyPositionsT_1,'PNL% Buy Pos. (T+1)':-PNLSellPositionsT_1,'Magnitue Of Arbitrage':0}
		arbitrageBuySellSignals['Over Bought/Sold'] = arbitrageBuySellSignals['Over Bought/Sold'].map({-111.0: 'Sell', 111.0: 'Buy'})
	else:
		pnlstatementforday = {'PNL% Sell Pos. (T+1)':PNLSellPositionsT_1,'PNL% Buy Pos. (T+1)':PNLBuyPositionsT_1,'Magnitue Of Arbitrage':0}
		arbitrageBuySellSignals['Over Bought/Sold'] = arbitrageBuySellSignals['Over Bought/Sold'].map({111.0: 'Sell', -111.0: 'Buy'})

	# Count the stats of Signal Right Buy, Right Sell, Total Buy & Total Sell
	resultDict=countRightSignals(arbitrageBuySellSignals)
	pnlstatementforday={**pnlstatementforday,**resultDict}

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
	return allData, pricedf, pnlstatementforday, scatterPlotData


# This function sends back PNL for all dates for ETF 
def retrievePNLForAllDays(etfname=None, magnitudeOfArbitrageToFilterOn=0):
	s=arbitragecollection.find({'ETFName':etfname})
	PNLOverDates={}
	# Iter over the collection results
	for i in s:
		allData, pricedf, pnlstatementforday, scatterPlotData=AnalyzeArbitrageDataForETF(arbitrageDataFromMongo=i, magnitudeOfArbitrageToFilterOn=magnitudeOfArbitrageToFilterOn)
		PNLOverDates[str(i['dateOfAnalysis'].date())]=pnlstatementforday
	return PNLOverDates



























