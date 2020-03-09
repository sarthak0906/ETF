from mongoengine import *
from datetime import datetime
import logging
from HoldingsDataScripts.ETFMongo import ETF
import pandas as pd

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig(filename="LoadEtfs.log", format='%(asctime)s %(message)s')


class LoadHoldingsdata(object):

    def __init__(self, etfname=None, fundholdingsdate='20200226'):
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
            if type(fundholdingsdate) is not datetime:
                fundholdingsdate = datetime.strptime(fundholdingsdate, "%Y%m%d").date()
            else:
                fundholdingsdate = fundholdingsdate.date()
            etfdata = ETF.objects(ETFTicker=etfname, FundHoldingsDate__lte=fundholdingsdate).order_by('-FundHoldingsDate').first()
            holdingsdatadf = pd.DataFrame(etfdata.to_mongo().to_dict()['holdings'])
            print(str(etfdata.FundHoldingsDate))
            return holdingsdatadf
        except Exception as e:
            print(e)
    
    def getETFWeights(self):
        return self.weights

    def getCashValue(self):
        return self.cashvalueweight

    def getSymbols(self):
        return self.symbols


