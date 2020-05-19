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
import ast
import json

sys.path.append("..")

app = Flask(__name__)

CORS(app)

# Production Local Server
# connect('ETF_db', alias='ETF_db')
# Production Server
connection=connect('ETF_db', alias='ETF_db', host='18.213.229.80', port=27017)

 
############################################
# Load ETF Holdings Data and Description
############################################



from FlaskAPI.Components.ETFDescription.helper import fetchETFsWithSameIssuer
@app.route('/GetEtfWithSameIssuer/<ETFName>/<date>')
def getETFWithSameIssuer(ETFName,date):
    etfswithsameIssuer = fetchETFsWithSameIssuer(connection,date,issuername)


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
        
        # ETFListWithSameIssuer
        etfswithsameIssuer=fetchETFsWithSameIssuer(connection,date,Issuer=ETFDataObject['Issuer'])
        if len(etfswithsameIssuer)==0:
            etfswithsameIssuer=['No other etf was found for issuer']
        
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

# Divide Columnt into movers and the price by which they are moving
etmoverslist=['ETFMover%1', 'ETFMover%2', 'ETFMover%3', 'ETFMover%4', 'ETFMover%5',
   'ETFMover%6', 'ETFMover%7', 'ETFMover%8', 'ETFMover%9', 'ETFMover%10',
   'Change%1', 'Change%2', 'Change%3', 'Change%4', 'Change%5', 'Change%6',
   'Change%7', 'Change%8', 'Change%9', 'Change%10']

@app.route('/PastArbitrageData/<ETFName>/<date>')
def FetchPastArbitrageData(ETFName, date):
    ColumnsForDisplay=['ETF Trading Spread in $','Arbitrage in $','Magnitude of Arbitrage','Over Bought/Sold Signal',
                        'ETFMOVER1','ETFMOVER2',
                        'MOVER1', 'MOVER2',
                        'T','T+1']

    # Retreive data for Components
    data, pricedf = RetrieveETFArbitrageData(ETFName, date)
    
    # Check if data doesn't exsist
    if data.empty:
        print("No Data Exist")
    
    
    # Seperate ETF Movers and the percentage of movement
    for movers in etmoverslist:
        def getTickerReturnFromMovers(x):
            #x = ast.literal_eval(x)
            return x[0],float(x[1])
        newcolnames = [movers+'_ticker',movers+'_value']
        data[movers]=data[movers].apply(getTickerReturnFromMovers)
        data[newcolnames]=pd.DataFrame(data[movers].tolist(), index=data.index) 
        del data[movers]

    # Sort the data frame on time since Sell and Buy are concatenated one after other
    data=data.sort_index()

    # Time Manpulation
    data.index =  data.index.time
    data.index=data.index.astype(str)

    # Round of DataFrame 
    data=data.round(3)

    # Replace Values in Pandas DataFrame
    data.rename(columns={'Flag':'Over Bought/Sold Signal',
        'ETFMover%1_ticker':'ETFMOVER1',
        'ETFMover%2_ticker':'ETFMOVER2',
        'Change%1_ticker':'MOVER1',
        'Change%2_ticker':'MOVER2'}, inplace=True)

    data['Over Bought/Sold Signal'] = data['Over Bought/Sold Signal'].map({111.0: 'Over Bought', -111.0: 'Over Sold'})
    
    
    # Get the price dataframe
    allData={}
    
    allData['etfPrices'] = pricedf[['Time','Close']].to_json(orient='records')
    
    # Columns needed to display
    data=data[ColumnsForDisplay]
    allData['etfhistoricaldata']=data.to_json(orient='index')
    print(allData)
    return json.dumps(allData)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

