import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import *
import sys
import json
import pandas as pd
from mongoengine import connect
import numpy as np
import math

sys.path.append("..")

app = Flask(__name__)

CORS(app)

# Production Local Server
# connect('ETF_db', alias='ETF_db')
# Production Server
connect('ETF_db', alias='ETF_db', host='18.213.229.80', port=27017)
 
############################################
# Load ETF Holdings Data and Description
############################################

from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
@app.route('/ETfDescription/<ETFName>/<date>')
@app.route('/ETfDescription/Holdings/<ETFName>/<date>')
@app.route('/ETfDescription/EtfData/<ETFName>/<date>')
def SendETFHoldingsData(ETFName, date):
    req=request.__dict__['environ']['REQUEST_URI']
    try:
        # Load all the data holdings data together
        etfdata = LoadHoldingsdata().getAllETFData(ETFName, date)
        ETFDataObject = etfdata.to_mongo().to_dict()
        
        # Holdings Data foe etf
        holdingsDatObject = pd.DataFrame(ETFDataObject['holdings']).set_index('TickerSymbol').to_json(orient='index')
        
        # ETF Description data
        # List of columns we don't need
        columnsNotNeeded = ['_id','DateOfScraping','ETFhomepage','holdings']
        for v in columnsNotNeeded:
            del ETFDataObject[v]
        ETFDataObject=pd.DataFrame(ETFDataObject,index=[0])
        ETFDataObject=ETFDataObject.replace(np.nan, 'nan', regex=True)
        ETFDataObject= ETFDataObject.loc[0].to_dict()
        # Remove 'NaN' from the data
        
        
        # Send back response depending on type of request
        if 'EtfData' in req:
            print(ETFDataObject)
            return ETFDataObject
        elif 'Holdings' in req:
            return holdingsDatObject
        else:
            return ETFDataObject, holdingsDatObject


    except Exception as e:
        print("Issue in Flask app while fetching ETF Description Data")
        print(e)
        return str(e)


############################################
# Load Past Arbitrage Past Data
############################################
from FlaskAPI.Components.ETFArbitrage.ETFArbitrageMain import RetrieveETFArbitrageData
@app.route('/PastArbitrageData/<ETFName>/<date>')
def FetchPastArbitrageData(ETFName, date):
    data = RetrieveETFArbitrageData(ETFName, date)
    data.index=data.index.astype(str)
    data=data.to_dict('index')
    print(data)
    return data


if __name__ == '__main__':
    app.run(port=5000, debug=True)

