import json
import sys, traceback
# For Piyush System
sys.path.extend(['/home/piyush/Desktop/etf1903', '/home/piyush/Desktop/etf1903/ETFsList_Scripts',
                 '/home/piyush/Desktop/etf1903/HoldingsDataScripts',
                 '/home/piyush/Desktop/etf1903/CommonServices',
                 '/home/piyush/Desktop/etf1903/CalculateETFArbitrage'])
# For Production env
sys.path.extend(['/home/ubuntu/ETFAnalysis', '/home/ubuntu/ETFAnalysis/ETFsList_Scripts',
                 '/home/ubuntu/ETFAnalysis/HoldingsDataScripts', '/home/ubuntu/ETFAnalysis/CommonServices',
                 '/home/ubuntu/ETFAnalysis/CalculateETFArbitrage'])
sys.path.append("..")  # Remove in production - KTZ
import datetime
import time
import pandas as pd
from CommonServices.ThreadingRequests import IOBoundThreading
from CommonServices.MultiProcessingTasks import CPUBonundThreading
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from CommonServices.RetryDecor import retry
import logging
import os
path = os.path.join(os.getcwd(), "Logs/")
if not os.path.exists(path):
    os.makedirs(path)

filename = path + datetime.datetime.now().strftime("%Y%m%d") + "-ArbPerMinLog.log"
handler = logging.FileHandler(filename)
logging.basicConfig(filename=filename, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='a')
# logger = logging.getLogger("EventLogger")
logger = logging.getLogger("ArbPerMinLogger")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

class tradestruct():
    def calc_pct_chg(self, priceT, priceT_1):
        return ((priceT-priceT_1)/priceT_1)*100

    def __init__(self, symbol, priceT, priceT_1=None):
        self.symbol = symbol
        self.priceT = priceT
        if not priceT_1:
            self.priceT_1 = priceT
        else:
            self.priceT_1 = priceT_1
        self.price_pct_chg = self.calc_pct_chg(self.priceT,self.priceT_1)

class LiveArbitragePerMinute():
    def __init__(self):
        self.tradedict = {}
    # def maketickerlists(self):
    #     self.etflist = list(pd.read_csv("/home/piyush/Desktop/etf1903/CalculateETFArbitrage/WorkingETFs.csv").columns.values)
    #     self.tickerlist = list(pd.read_csv("/home/piyush/Desktop/etf1903/tickerlist.csv").columns.values)
    #     self.tickerlistStr = ','.join([str(elem) for elem in self.tickerlist])
    #     print(self.tickerlistStr)
    #     f = open('/home/piyush/Desktop/etf1903/etf-hold.json', 'r')
    #     self.etfdict = json.load(f)
    #     self.tradedict = {}

    def PolygonLastQuotes(self, symbol):
        # Make use of Tickers
        requesturl = 'https://api.polygon.io/v1/last_quote/stocks/' + symbol + '?apiKey=M_PKVL_rqHZI7VM9ZYO_hwPiConz5rIklx893F'
        return requesturl

    def makeurllists(self):
        self.lastquotesurls = [self.PolygonLastQuotes(etf) for etf in self.etflist]
        self.lasttradeurls = [PolgonDataCreateURLS().PolygonLastTrades(ticker.replace("AM.", "")) for ticker in self.tickerlist]


##############################################################################
    @retry(exceptions=Exception, total_tries=2, initial_wait=0.5, backoff_factor=1, logger=logger)
    def getDataFromPolygon(self, methodToBeCalled=None, getUrls=None):
        # Calling IO Bound Threading to fetch data for URLS
        if methodToBeCalled == None or getUrls == None:
            return None
        responses = IOBoundThreading(getUrls)
        ResultsfromResponses = CPUBonundThreading(methodToBeCalled, responses)
        return ResultsfromResponses


    def extractQuotesDataFromResponses(self, response):
        try:
            symbol = response['symbol']
            tradingspread = response['last']['askprice'] - response['last']['bidprice']
            responseData = {'ticker': symbol, 'Spread': tradingspread}
        except:
            # print("No quotes data for {}".format(response['symbol']))
            responseData = None
            pass
        return responseData


    def extractTradesDataFromResponses(self, response):
        try:
            symbol = response['symbol']
            price = response['last']['price']
            if symbol in self.tradedict.keys():
                priceT_1 = self.tradedict[symbol].priceT
                tradeobj = tradestruct(symbol=symbol,priceT=price,priceT_1=priceT_1)
                self.tradedict[symbol] = tradeobj
            else:
                tradeobj = tradestruct(symbol=symbol,priceT=price)
                self.tradedict[symbol] = tradeobj
            # responseData = {'ticker': symbol, 'price': price}
        except:
            # print("No trades data for {}".format(response['symbol']))
            # responseData = None
            pass
        # return responseData



    def calcArbitrage(self):
        self.getDataFromPolygon(self.extractTradesDataFromResponses,self.lasttradeurls)
        self.tradedf = pd.DataFrame(columns=['symbol', 'priceT', 'priceT_1', 'price_pct_chg'])
        for key, value in self.tradedict.items():
            valdict = value.__dict__
            self.tradedf = self.tradedf.append(valdict,ignore_index=True)
        self.arbdict = {}
        self.tradedf.set_index('symbol', inplace=True)
        for etf in self.etfdict:
            for etfname, holdingdata in etf.items():
                try:
                    df = None
                    summation = 0
                    # ETF Price Change % calculation
                    etfchange = self.tradedf.loc[etfname, 'price_pct_chg']
                    # NAV change % Calculation
                    for holdings in holdingdata:
                        df = pd.DataFrame(holdings)
                    df.set_index('symbol', inplace=True)
                    for sym in df.index:
                        prod = (df.loc[sym, 'weight']) * (self.tradedf.loc[sym, 'price_pct_chg'])
                        summation = summation + prod
                    # summation = NAV change %
                    etfprice = self.tradedf.loc[etfname, 'priceT']
                    arbitrage = ((etfchange - summation) * etfprice) / 100
                    self.arbdict.update({etfname: arbitrage})
                except Exception as e:
                    # print(e)
                    # traceback.print_exc(file=sys.stdout)
                    pass
        return self.arbdict

    def main(self):
        self.etflist = list(
            pd.read_csv("CalculateETFArbitrage/WorkingETFs.csv").columns.values)
        self.tickerlist = list(pd.read_csv("CalculateETFArbitrage/tickerlist.csv").columns.values)
        self.tickerlistStr = ','.join([str(elem) for elem in self.tickerlist])
        # print(self.tickerlistStr)
        f = open('CalculateETFArbitrage/etf-hold.json', 'r')
        self.etfdict = json.load(f)

        self.makeurllists()
        while True:
            quotesresults = self.getDataFromPolygon(self.extractQuotesDataFromResponses, self.lastquotesurls)
            resultsq = [x for x in quotesresults if x]
            spreadDF = pd.DataFrame(resultsq)
            spreadDF.set_index('ticker', inplace=True)
            arbitdict = self.calcArbitrage()
            arbDF = pd.DataFrame.from_dict(arbitdict, orient='index',columns=['arbitrage'])
            mergeDF = arbDF.merge(spreadDF, left_index=True, right_index=True)
            yield mergeDF


# livarb = LiveArbitragePerMinute()
# # livarb.maketickerlists()
# # livarb.makeurllists()
# while True:
#     dt = datetime.datetime.now() + datetime.timedelta(minutes=1)
#     resultgen = livarb.main()
#     print("ResultDF : ")
#     print(next(resultgen))
#     print(dt - datetime.datetime.now())
#     while datetime.datetime.now() < dt:
#         time.sleep(1)
