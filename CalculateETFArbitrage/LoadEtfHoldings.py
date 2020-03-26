from mongoengine import *
from datetime import datetime
import logging
from HoldingsDataScripts.ETFMongo import ETF
import pandas as pd

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig(filename="LoadEtfs.log", format='%(asctime)s %(message)s')


class LoadHoldingsdata(object):

    def __init__(self, etfname=None, fundholdingsdate=None):
        try:
            holdings = self.getHoldingsDatafromDB(etfname, fundholdingsdate)
            holdings['TickerWeight'] = holdings['TickerWeight'] / 100
            # Assign cashvalueweight 
            self.cashvalueweight = holdings[holdings['TickerSymbol'] == 'CASH'].get('TickerWeight').item()

            # Assign Weight %
            self.weights = dict(zip(holdings.TickerSymbol, holdings.TickerWeight))

            # Assign symbols
            symbols = holdings['TickerSymbol'].tolist()
            symbols.append(etfname)
            symbols.remove('CASH')
            self.symbols = symbols
            
            log.info("Data Successfully Loaded")
        except Exception as e:
            log.error("Data Not Loaded")
            logging.critical(e, exc_info=True)

    def getHoldingsDatafromDB(self, etfname, fundholdingsdate):
        try:
            
            connect('ETF_db', alias='ETF_db')
            print(etfname)                  
            print(fundholdingsdate)                     
            etfdata = ETF.objects(ETFTicker=etfname).order_by('-FundHoldingsDate').first()
            '''
            # connect('ETF_db', alias='ETF_db')
            # Connecting to ETF_db on AWS EC2 Production Server
            connect('ETF_db', alias='ETF_db', host='52.91.26.227', port=27017)
            etfdata = ETF.objects(ETFTicker=etfname, FundHoldingsDate__lte=fundholdingsdate).order_by(
                '-FundHoldingsDate').first()
            '''
            print(etfdata)
            holdingsdatadf = pd.DataFrame(etfdata.to_mongo().to_dict()['holdings'])
            print(str(etfdata.FundHoldingsDate))
            return holdingsdatadf
        except Exception as e:
            print("Can't Fetch Fund Holdings Data")
            print(e)

    def getHoldingsDataForAllETFfromDB(self, etfname):
        try:
            # connect('ETF_db', alias='ETF_db')
            # Connecting to ETF_db on AWS EC2 Production Server
            connect('ETF_db', alias='ETF_db', host='52.91.26.227', port=27017)
            etfdata = ETF.objects(ETFTicker=etfname).order_by('-FundHoldingsDate').first()
            print(etfdata.ETFTicker)
            holdingsdatadf = pd.DataFrame(etfdata.to_mongo().to_dict()['holdings'])
            print(str(etfdata.FundHoldingsDate))
            return holdingsdatadf['TickerSymbol'].to_list()
        except Exception as e:
            print("Can't Fetch Fund Holdings Data for all ETFs")
            print(e)

    def getETFWeights(self):
        return self.weights

    def getCashValue(self):
        return self.cashvalueweight

    def getSymbols(self):
        return self.symbols


