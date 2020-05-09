from flask import Flask, request, jsonify
from mongoengine import *

app = Flask(__name__)

@app.route('/<ETFName>/<date>')
def SendETFData():
    # Get the data from the POST request.
    data = request.get_json(force=True)

    try:
        # Production username = ubuntu
        if getpass.getuser() == 'ubuntu':
            # Connect to localhost server for Production
            connect('ETF_db', alias='ETF_db')
        else:
            # Connecting to ETF_db on AWS EC2 Production Server
            connect('ETF_db', alias='ETF_db', host='18.213.229.80', port=27017)
        etfdata = ETF.objects(ETFTicker=etfname, FundHoldingsDate__lte=fundholdingsdate).order_by(
            '-FundHoldingsDate').first()
        print(etfdata)
        holdingsdatadf = pd.DataFrame(etfdata.to_mongo().to_dict()['holdings'])
        print(str(etfdata.FundHoldingsDate))
        disconnect('ETF_db')
        return holdingsdatadf

    except Exception as e:
        print("Can't Fetch Fund Holdings Data")
        print(e)
        logger.exception(e)
        logger2.exception(e)
        # logger.critical(e, exc_info=True)
        disconnect('ETF_db')

    output = prediction[0]

    return jsonify(output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)