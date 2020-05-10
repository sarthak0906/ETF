import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import *
import sys
import json
import pandas as pd

sys.path.append("..")

# Import packages
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata


app = Flask(__name__)

CORS(app)

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
        holdingsDatObject = pd.DataFrame(ETFDataObject['holdings']).to_json(orient='index')
        
        # ETF Description data
        # List of columns we don't need
        columnsNotNeeded = ['_id','DateOfScraping','ETFhomepage','holdings']
        for v in columnsNotNeeded:
            del ETFDataObject[v]
        
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)

