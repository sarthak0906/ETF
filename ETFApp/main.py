import sys
sys.path.insert(0, 'lib')

# importing packages for twitter
import json
import numpy
import pandas as pd
from datetime import datetime

# import flask modules
from flask import render_template, request, send_from_directory, jsonify
from flask import Flask

# import custom python packages
from DataGatheringCleaning import *
from JingaDataCleanUp import CleanDataForJinga,CleanETFDailyData
from ArbitrageAnalysis import *

from MongoReadETFData import RetrieveData

app = Flask(__name__,
		static_url_path='', 
        static_folder='static',
        template_folder='templates')


@app.route('/AnalyseEtf')
def index():
	return render_template('index.html',)

@app.route('/ETFHistoricalDaily',methods= ['POST','GET'])
def analyseDailyMispricing():
	ob=RetrieveData()
	date=datetime(2020,2,7)
	query={'FundHoldingsDate':date}
	data=ob.queryData(query)
	

	data=CleanETFDailyData(data).execute()
	print(data)
	return render_template('DailyMispricing.html',DailyMispricingData=data,date=date)


@app.route('/AnalyseEtf/<etfticker>',methods= ['POST','GET'])
def handle(**kwargs):
	tickeretf = request.form['ticker']
	stdthresold = float(request.form['stdthresold'])

	print("Ticker is = "+tickeretf)
	print("Tracking Error is = "+str(stdthresold))

	filename='../ETFDailyData'+'/'+'20200207'+'/'+tickeretf+'.xls'
	startdate=dt.datetime(2019,1,1)
	enddate=dt.datetime.today()

	###$$$ Getting ticker prices, cleaning them and finding NET Asset Valu
	# Create an object of Constituents Data of ETF - ConstituentsData
	ob=ConstituentsData()
	# Load ETF Weights
	etfWeights=ob.loadETFWeights(filename)
	# Get Stock Prices from the weights
	ob.getStockPrices(startdate=startdate,enddate=enddate)
	# ShowNa Values - Method Inherited from ETFDataCleanup
	print("If ETF constituents has any NA Values")
	ob.showNaColumns(ob.constituentcloseDF)
	# Drop Na Values from above - Method Inherited from ETFDataCleanup
	ob.constituentcloseDF=ob.dropNAColumns(ob.constituentcloseDF)
	# Computre Daily Returs - Method Inherited from ETFDataCleanup
	ob.changeDF=ob.computeDailyReturns(ob.constituentcloseDF)
	# Weights in weights file have weights in % Clean that up
	ob.stringWeightsToFloat()
	# Find Net Asset Values
	ob.findNetAssetValue()

	###$$$ Getting data for ETF starts here
	# Object to Get ETF Data
	etfob=ETFStockPrices(etfticker=tickeretf)
	# Get ETF Data Stock Prices
	etfob.getETFTickerData(startdate=startdate,enddate=enddate)
	# Show Any Na Values
	print("If ETF prices has any NA Values")
	etfob.showNaColumns(etfob.etfdata)
	# Calculate daily returns of ETF
	etfob.etfchangeDF=etfob.computeDailyReturns(etfob.etfdata['Close'])

	###$$$ Calculation for Arbitrage Starts Here
	# Do Calculations of ETFArbitrage
	arbob=ETFArbitrage(etfob.etfchangeDF,ob.weightedStockReturns)
	daysofarbitrage, tickersSTDdata=ArbitrageAnalysis().GetArbDataFrame(tickers=ob.constituentcloseDF.columns,changeDF=ob.changeDF,constituentdata=ob.constituentdata,daysofarbitrage=round(arbob.navDF.copy(),3),stdthresold=stdthresold)

	# Get ZScores for Constituents On Day of Arbitrage
	dateForZScore=daysofarbitrage.index[0]
	zscoresOfConstituents=ArbitrageAnalysis().getZScoresOnDate(dateForZScore,tickersSTDdata)

	###$$$ Maniputaion of data for Jinga Template Starts Here	
	# Round Off NavDf and Clean up for printing
	navDF=CleanDataForJinga(round(arbob.navDF.copy(),3),['Date','Close','NAV','Mispricing'],'Date',reverse=True).CleanForEndUser()
	# Round Off constituentsdata and Clean up for printing
	constituentsdata=CleanDataForJinga(ob.etfWeights.copy(),['Ticker','Company Name','Weights','Last','%Change','Volume'],'Ticker',reverse=False).CleanForEndUser()
	# Round Off daysofarbitrage and Clean up for printing
	daysofarbitrage=CleanDataForJinga(daysofarbitrage,['Date','Close','NAV','Mispricing Z-Score','Mispricing'],'Date',reverse=True).CleanForEndUser()
	# Cleaning df of Zscores of constituents
	zscoresOfConstituents=CleanDataForJinga(zscoresOfConstituents,['Ticker','Return Z-Score','Vol. Wgt Return Z-Score','Vol. Z-Score'],'Ticker',reverse=True).CleanForEndUser()

	return render_template('RenderEtfView.html',tickeretf=tickeretf,stdthresold=stdthresold,daysofarbitrage=daysofarbitrage,navDF=navDF,constituentsdata=constituentsdata,zscoresOfConstituents=zscoresOfConstituents,dateForZScore=dateForZScore)


if __name__ == '__main__':
    app.run(debug=True)



