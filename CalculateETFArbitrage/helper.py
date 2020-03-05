import pandas as pd
import numpy as np
from datetime import datetime
import time
from mongoengine import *

from PolygonTickData.PolygonDataAPIConnection import PolgonData
from HoldingsDataScripts.ETFMongo import ETF
from HoldingsDataScripts.HoldingsMongo import Holdings
###################################################################
### Use this class for performing actions and keep code clean  ####
###################################################################

class Helper(object):

    def __init__(self):
        pass

    def convertDictToFrame(self, data):
        finalDF = []
        for key, value in data.items():
            df = pd.DataFrame.from_dict(value[key]['results'])
            df['Symbol'] = key
            finalDF.append(df)
        return pd.concat(finalDF)

    # Returns timestamp with milliseconds
    def unix_time_millis(self, dt):
        epoch = datetime.utcfromtimestamp(0)
        tsDate = (dt - epoch).total_seconds() * 1000.0
        tsDate = str(int(tsDate)) + '000000'
        return tsDate

    def stringTimeToDatetime(self, date=None, time=None):
        marketOpenTSStr = date + ' ' + time
        return datetime.strptime(marketOpenTSStr, '%Y-%m-%d %H:%M:%S')

    def convertStringDateToTS(self, date=None, starttime='9:30:00', endtime='17:00:00'):
        marketOpenTSStr = date + ' ' + starttime
        marketCloseTSStr = date + ' ' + endtime

        marketTimeStamps = {}
        marketTimeStamps['marketOpenTS'] = self.unix_time_millis(
            datetime.strptime(marketOpenTSStr, '%Y-%m-%d %H:%M:%S'))
        marketTimeStamps['marketCloseTS'] = self.unix_time_millis(
            datetime.strptime(marketCloseTSStr, '%Y-%m-%d %H:%M:%S'))
        return marketTimeStamps

    def getHumanTime(self, ts, getMilliSecondsAlso=False):
        try:
            s, ms = divmod(ts, 1000000000)
            if getMilliSecondsAlso:
                return datetime(*time.gmtime(s)[:6]), ms
            else:
                return datetime(*time.gmtime(s)[:6])
        # print('{}.{:03d}'.format(time.strftime('%Y-%m-%d %H:%M:%S',  time.gmtime(s)), ms))
        except AttributeError:
            print("Attribute Error Occured")
            print(ts)
            print(s)
            print(ms)

    def getHoldingsDatafromDB(self, etfname, fundholdingsdate):
        try:
            connect('ETF_db', alias='ETF_db')
            fundholdingsdate = datetime.strptime(fundholdingsdate, "%Y%m%d").date()
            etfdata = ETF.objects(ETFTicker=etfname, FundHoldingsDate__lte=fundholdingsdate).order_by('-FundHoldingsDate').first()
            holdingsdatadf = pd.DataFrame(etfdata.to_mongo().to_dict()['holdings'])
            print(str(etfdata.FundHoldingsDate))
            return holdingsdatadf
        except Exception as e:
            print(e)

#############
### Threading - not beig used rigt now
#############

import aiohttp
import asyncio


class ThreadingGetRequests(object):

    def __init__(self, urls):
        # Pass Your Thread request here
        self.urls = [
            'http://python.org',
            'https://google.com',
            'http://yifei.me'
        ]

    def startThreading(self):
        async def fetch(session, url):
            async with session.get(url) as response:
                return await response.text()

        async def main():
            tasks = []
            async with aiohttp.ClientSession() as session:
                for url in self.urls:
                    print(url)
                    tasks.append(fetch(session, url))
                htmls = await asyncio.gather(*tasks)

                for html in htmls:
                    print("******")
                    print(html[:100])

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

# ob=ThreadingGetRequests(urls=['Kshitiz','Sharma'])
# ob.startThreading()

