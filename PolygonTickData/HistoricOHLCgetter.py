from pymongo import *
from CommonServices.ThreadingRequests import IOBoundThreading
from CommonServices.MultiProcessingTasks import CPUBonundThreading
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from dateutil.rrule import *
import datetime


class HistoricOHLC():
    def getDailyOpenCloseSinceInceptionFromPolygon(self, getUrls=None):
        # Calling IO Bound Threading to fetch data for URLS
        if getUrls == None:
            return None
        responses = IOBoundThreading(getUrls)
        ResultsfromResponses = CPUBonundThreading(self.extractDailyOpenCloseSinceInceptionDataFromResponses, responses)
        return ResultsfromResponses

    def extractDailyOpenCloseSinceInceptionDataFromResponses(self, response):
        try:
            from_time = response['from']
            symbol = response['symbol']
            open = response['open']
            high = response['high']
            low = response['low']
            close = response['close']
            afterHours = response['afterHours']
            volume = response['volume']
            # Response returned in form of Dict
            responseData = {'from': from_time, 'symbol': symbol, 'open': open, 'high': high, 'low': low, 'close': close,
                            'afterHours': afterHours, 'volume': volume}
        except:
            # print("No quotes data for {}".format(response['symbol']))
            responseData = None
            pass
        return responseData

    def getopenlowhistoric(self, etfname):
        connection = MongoClient('localhost', 27017)
        db = connection.ETF_db
        inceptiondate_data = db.ETFHoldings.find({"ETFTicker": etfname}, {"_id": 0, "InceptionDate": 1}).sort(
            "FundHoldingsDate", -1).limit(1)
        startdt = [date['InceptionDate'] for date in inceptiondate_data][0]
        nat_holidays = ['2020-01-01', '2020-01-20', '2020-02-17', '2020-05-25', '2020-07-03', '2020-07-04',
                        '2020-09-07',
                        '2020-10-12', '2020-11-11', '2020-11-26', '2020-12-25']
        working_days = list(rrule(WEEKLY, byweekday=(MO, TU, WE, TH, FR), dtstart=startdt,
                                  until=datetime.datetime.now()))
        urls = [
            PolgonDataCreateURLS().PolygonDailyOpenClose(date=datetime.datetime.strftime(date, "%Y-%m-%d"),
                                                         symbol='XLK')
            for date in working_days]
        responsedata = self.getDailyOpenCloseSinceInceptionFromPolygon(getUrls=urls)
        data = [data for data in responsedata if data is not None]
        return data
