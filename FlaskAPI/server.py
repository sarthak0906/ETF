import sys
from flask import Flask, request, jsonify
from mongoengine import *
sys.path.append("..")

from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata

app = Flask(__name__)

@app.route('/<ETFName>/<date>')
def SendETFData(ETFName, date):
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)