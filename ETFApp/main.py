import sys
sys.path.insert(0, 'lib')

# importing packages for twitter
import json
import numpy
import pandas as pd

# Import flask modules
from flask import render_template, request, send_from_directory, jsonify
from flask import Flask

import pickle

from StandardDeviationAnalysis import *

app = Flask(__name__,
		static_url_path='', 
        static_folder='static',
        template_folder='templates')


@app.route('/')
def index():
	return render_template('index.html',)


@app.route('/getETF',methods= ['POST'])
def getETF():
	try:
		tickeretf = request.form['ticker']
	except:
		tickeretf="XLK"

	print("Ticker is ="+tickeretf)
	
	
	filename='../ETFDailyData'+'/'+dt.datetime.now().strftime("%Y%m%d")+'/'+tickeretf+'.xls'
	startdate=dt.datetime(2019,1,1)
	enddate=dt.datetime.today()

	ob=ConstituentsData(fileName=filename,startdate=startdate,enddate=enddate)
	ob.getconstituentdata()
	
	print("Ticker is ="+tickeretf)
	print("***************")
	print("Tickers with NA Values")
	ob.showNaColumns(ob.constituentcloseDF)
	ob.constituentcloseDF=ob.dropNAColumns(ob.constituentcloseDF)
	print("***************")
	print("Check for NA Values again")
	ob.showNaColumns(ob.constituentcloseDF)
	ob.changeDF=ob.computeDailyReturns(ob.constituentcloseDF)
	print("***************")
	print("Daily Change of Constituents")
	print(ob.changeDF.tail(10))


	ob.stringWeightsToFloat()
	ob.findNetAssetValue()

	print("***************")
	print("Data for Constituents")
	print(ob.waDF.head(5))

	etfob=ETFStockPrices(etfticker=tickeretf,startdate=startdate,enddate=enddate)
	etfob.getETFTickerData()
	print("***************")
	print("Show Any Empty Values for ETF")
	etfob.showNaColumns(etfob.etfdata)
	etfob.etfchangeDF=etfob.computeDailyReturns(etfob.etfdata['Close'])

	arbob=ETFArbitrage(etfob.etfchangeDF,ob.waDF)
	print("***************")
	print("Show NAV DF")
	print(arbob.navDF)

	# Format the NAVDf Dataframe for Printing
	navDF=round(arbob.navDF.copy(),3)
	navDF['Date']=navDF.index
	navDF=navDF[['Date','Close','NAV','Mispricing','Z-Score']]
	navDF=navDF.reset_index(drop=True)

	# Format the Constituents Dataframe for printing
	constituentsdata=ob.tickerdf.copy()
	constituentsdata['Ticker']=constituentsdata.index
	constituentsdata=constituentsdata[['Ticker','Company Name','Weights','Last','%Change','Volume']]
	constituentsdata=constituentsdata.reset_index(drop=True)
	return render_template('RenderEtfView.html',navDF=navDF,constituentsdata=constituentsdata)


if __name__ == '__main__':
    app.run(debug=True)



