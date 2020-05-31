from pymongo import *
from CommonServices.ThreadingRequests import IOBoundThreading
from CommonServices.MultiProcessingTasks import CPUBonundThreading
from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from dateutil.rrule import *
import datetime
import pandas as pd

class HistoricOHLC():
    def getDailyOpenCloseSinceInceptionFromPolygon(self, getUrls=None):
        responses = IOBoundThreading(getUrls)
        return responses

    def getopenlowhistoric(self, etfname=None, startdate=None):
        todaysDate = datetime.datetime.today().strftime('%Y-%m-%d')
        url  = PolgonDataCreateURLS().PolygonAggregdateData(symbol=etfname, aggregateBy='day', startDate=startdate, endDate=todaysDate)
        responsedata = self.getDailyOpenCloseSinceInceptionFromPolygon(getUrls=[url])
        result=responsedata[0]['results']
        result=pd.DataFrame(result)
        print(result)
        return result
