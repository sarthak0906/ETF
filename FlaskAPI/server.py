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
from datetime import datetime
sys.path.append("..")

app = Flask(__name__)

CORS(app)

# Production Local Server
# connect('ETF_db', alias='ETF_db')
# Production Server
connection = connect('ETF_db', alias='ETF_db', host='18.213.229.80', port=27017)


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
    req = request.__dict__['environ']['REQUEST_URI']
    try:
        # Load all the data holdings data together
        etfdata = LoadHoldingsdata().getAllETFData(ETFName, date)
        ETFDataObject = etfdata.to_mongo().to_dict()

        # Holdings Data foe etf
        holdingsDatObject = pd.DataFrame(ETFDataObject['holdings']).to_dict(orient='records')

        # ETF Description data
        # List of columns we don't need
        # Delete
        columnsNotNeeded = ['_id', 'DateOfScraping', 'ETFhomepage', 'holdings']
        for v in columnsNotNeeded:
            del ETFDataObject[v]
        # ETFListWithSameIssuer
        etfswithsameIssuer=fetchETFsWithSameIssuer(connection,date,Issuer=ETFDataObject['Issuer'])
        if len(etfswithsameIssuer)==0:
            etfswithsameIssuer=['No other etf was found for issuer']
        else:
            # print(etfswithsameIssuer, file=open('a.txt', 'w'))
            WithSameIssuer = []
            for key in etfswithsameIssuer[0]:
                WithSameIssuer.append({'Symbol': key, 'Name': etfswithsameIssuer[0][key], 'Value': etfswithsameIssuer[1][key]})
            etfswithsameIssuer = pd.DataFrame(WithSameIssuer).to_dict(orient='records')
            print(etfswithsameIssuer, file=open('a.txt', 'w'))
        
        del ETFDataObject['FundHoldingsDate']
        ETFDataObject['InceptionDate']=str(ETFDataObject['InceptionDate'])

        ETFDataObject = pd.DataFrame(ETFDataObject.items())
        ETFDataObject = ETFDataObject.replace(np.nan, 'nan', regex=True)
        ETFDataObject = ETFDataObject.to_dict(orient='records')



        # Send back response depending on type of request
        if 'EtfData' in req:
            allData={}
            allData['ETFDataObject'] = ETFDataObject
            allData['etfswithsameIssuer'] = etfswithsameIssuer

            print(etfswithsameIssuer)

            return json.dumps(allData)
        elif 'Holdings' in req:
            return json.dumps(holdingsDatObject)
        else:
            allData={}
            allData['ETFDataObject'] = ETFDataObject
            allData['holdingsDatObject'] = holdingsDatObject
            allData['etfswithsameIssuer'] = etfswithsameIssuer
            return json.dumps(allData)
    except Exception as e:
        print("Issue in Flask app while fetching ETF Description Data")
        print(e)
        return str(e)


############################################
# Load Past Arbitrage Past Data
############################################
from FlaskAPI.Components.ETFArbitrage.ETFArbitrageMain import RetrieveETFArbitrageData, retrievePNLForAllDays

# Divide Columnt into movers and the price by which they are moving
etmoverslist = ['ETFMover%1', 'ETFMover%2', 'ETFMover%3', 'ETFMover%4', 'ETFMover%5',
                'ETFMover%6', 'ETFMover%7', 'ETFMover%8', 'ETFMover%9', 'ETFMover%10',
                'Change%1', 'Change%2', 'Change%3', 'Change%4', 'Change%5', 'Change%6',
                'Change%7', 'Change%8', 'Change%9', 'Change%10']


@app.route('/PastArbitrageData/<ETFName>/<date>')
def FetchPastArbitrageData(ETFName, date):
    ColumnsForDisplay = ['$Spread', '$Arbitrage', 'Absolute Arbitrage',
                         'Over Bought/Sold',
                         'Etf Mover',
                         'Most Change%',
                         'T', 'T+1']

    # Retreive data for Components
    data, pricedf, PNLStatementForTheDay, scatterPlotData = RetrieveETFArbitrageData(etfname=ETFName, date=date, magnitudeOfArbitrageToFilterOn=0)

    # Check if data doesn't exsist
    if data.empty:
        print("No Data Exist")
    
    ########### Code to modify the ETF Movers and Underlying with highest change %
    # Seperate ETF Movers and the percentage of movement
    for movers in etmoverslist:
        def getTickerReturnFromMovers(x):
            # x = ast.literal_eval(x)
            return x[0], float(x[1])

        newcolnames = [movers + '_ticker', movers + '_value']
        data[movers] = data[movers].apply(getTickerReturnFromMovers)
        data[newcolnames] = pd.DataFrame(data[movers].tolist(), index=data.index)
        del data[movers]

    etfmoversList = dict(data[['ETFMover%1_ticker','ETFMover%2_ticker','ETFMover%3_ticker']].stack().value_counts())
    etfmoversDictCount = pd.DataFrame.from_dict(etfmoversList,orient='index',columns=['Count']).to_dict('records')

    highestChangeList=dict(data[['Change%1_ticker','Change%2_ticker','Change%3_ticker']].stack().value_counts())
    highestChangeDictCount=pd.DataFrame.from_dict(highestChangeList,orient='index',columns=['Count']).to_dict('index')
    ########## Code to modify the ETF Movers and Underlying with highest change %


    # Sort the data frame on time since Sell and Buy are concatenated one after other
    data = data.sort_index()

    # Time Manpulation
    data.index = data.index.time
    data.index = data.index.astype(str)

    # Round of DataFrame 
    data = data.round(3)
    print(data.head())

    # Replace Values in Pandas DataFrame
    data.rename(columns={'ETF Trading Spread in $':'$Spread',
                        'Arbitrage in $':'$Arbitrage',
                        'Magnitude of Arbitrage':'Absolute Arbitrage',
                        'ETFMover%1_ticker': 'Etf Mover',
                        'Change%1_ticker': 'Most Change%'}, inplace=True)

    # Get the price dataframe
    allData={}
    # Columns needed to display
    data = data[ColumnsForDisplay]
    
    # PNL for all dates for the etf
    allData['etfhistoricaldata'] = data.to_dict(orient='records')
    print("Price Df")
    print(pricedf)
    allData['etfPrices'] = pricedf.to_csv(sep='\t',index=False)
    allData['PNLStatementForTheDay'] = pd.DataFrame(PNLStatementForTheDay.items()).to_dict(orient='records')
    print(pd.DataFrame(PNLStatementForTheDay.items()).to_dict(orient='records'))
    allData['scatterPlotData'] = json.dumps(scatterPlotData)
    allData['etfmoversDictCount']=json.dumps(etfmoversDictCount)
    allData['highestChangeDictCount']=json.dumps(highestChangeDictCount)
    return json.dumps(allData)


@app.route('/PastArbitrageData/CommonDataAcrossEtf/<ETFName>')
def fetchPNLForETFForALlDays(ETFName):
    print("All ETF PNL Statement is called")
    PNLOverDates=retrievePNLForAllDays(etfname=ETFName, magnitudeOfArbitrageToFilterOn=0)
    allData={}
    print(PNLOverDates)
    PNLOverDates = pd.DataFrame(PNLOverDates, index=False).set_index('date')
    print(PNLOverDates)
    PNLOverDates = PNLOverDates.to_dict(orient='records')
    allData['PNLOverDates'] = json.dumps(PNLOverDates)
    return allData


############################################
# Live Arbitrage
############################################

from MongoDB.PerMinDataOperations import PerMinDataOperations


@app.route('/ETfLiveArbitrage/AllTickers')
def SendLiveArbitrageDataAllTickers():
    req = request.__dict__['environ']['REQUEST_URI']
    try:
        live_data = PerMinDataOperations().FetchPerMinLiveData()
        live_prices = PerMinDataOperations().FetchAllETFPricesLive()

        live_prices_data = []
        [live_prices_data.append(item) for item in live_prices]

        data2 = []
        [data2.extend(item['ArbitrageData']) for item in live_data]

        prices_df = pd.DataFrame.from_records(live_prices_data)
        prices_df.rename(columns={'sym':'Symbol', 'vw':'Price', 'e':'Timestamp'}, inplace=True)
        df = pd.DataFrame.from_records(data2)
        ndf = df.merge(prices_df, how='left',on='Symbol')
        ndf.dropna(inplace=True)
        return json.dumps(ndf.to_dict(orient='records'))
    except Exception as e:
        print("Issue in Flask app while fetching ETF Description Data")
        print(e)
        return str(e)


@app.route('/ETfLiveArbitrage/Single/<etfname>')
def SendLiveArbitrageDataSingleTicker(etfname):
    req = request.__dict__['environ']['REQUEST_URI']
    try:
        etf_full_day_price_cursor = PerMinDataOperations().FetchFullDayPricesForETF(etfname)
        etf_full_day_price_data = []
        [etf_full_day_price_data.append(item) for item in etf_full_day_price_cursor]
        full_day_prices_df = pd.DataFrame.from_records(etf_full_day_price_data)
        full_day_prices_df.rename(columns={'sym':'Symbol', 'vw':'Price', 'e':'Timestamp'}, inplace=True)
        full_day_prices_df.drop(columns=['Symbol'], inplace=True)
        # print(full_day_prices_df)

        live_data = PerMinDataOperations().FetchPerMinLiveData(etfname=etfname)
        data1 = []
        [data1.append({'Timestamp': item['Timestamp'], 'Symbol': item['ArbitrageData'][0]['Symbol'],
                       'Arbitrage': item['ArbitrageData'][0]['Arbitrage'],
                       'Spread': item['ArbitrageData'][0]['Spread']}) for item in live_data]
        live_data_df = pd.DataFrame.from_records(data1)

        full_day_data = PerMinDataOperations().FetchPerMinArbitrageFullDay(etfname=etfname)
        data = []
        [data.append({'Timestamp': item['Timestamp'], 'Symbol': item['ArbitrageData'][0]['Symbol'],
                      'Arbitrage': item['ArbitrageData'][0]['Arbitrage'], 'Spread': item['ArbitrageData'][0]['Spread']})
         for item in full_day_data]
        full_day_data_df = pd.DataFrame.from_records(data)

        mergedDF = full_day_data_df.merge(full_day_prices_df, on='Timestamp', how='left')
        print(mergedDF)
        # live_data_df = mergedDF.loc[mergedDF['Timestamp'].idxmax()]
        # live_data_dict = live_data_df.to_dict()

        # return "Live: {}, Full_Day: {}".format(live_data_df.to_dict(), full_day_data_df.to_dict())
        return jsonify(Live=live_data_df.to_dict(orient='records'), Full_Day=mergedDF.to_dict(orient='records'))

    except Exception as e:
        print("Issue in Flask app while fetching ETF Description Data")
        print(e)
        return str(e)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
