import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import *
import sys
sys.path.append("..")

from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata

app = Flask(__name__)

CORS(app)

@app.route('/Holdings/<ETFName>/<date>')
def SendETFHoldingsData(ETFName, date):
    # Get the data from the POST request.
    # data = request.get_json(force=True)

    try:
        ETFDataOBJ = LoadHoldingsdata()
        holdingsdatadf =  ETFDataOBJ.getHoldingsDatafromDB(ETFName, date)
        return holdingsdatadf.to_json(orient='index')

    except Exception as e:
        print("Can't Fetch Fund Holdings Data")
        print(e)
        return str(e)

@app.route('/Description/<ETFName>/<date>')
def getETFDescriptionfromDB(ETFName, date):
    try:
        ETFDataOBJ = LoadHoldingsdata()
        holdingsdatadf =  ETFDataOBJ.getETFDescriptionfromDB(ETFName, date)
        # print(type(holdingsdatadf.to_dict(orient='index')))
        return  holdingsdatadf.to_dict(orient='index')[0]

    except Exception as e:
        print("Can't Fetch Fund Holdings Data on server")
        print(e)
        return str(e)
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)