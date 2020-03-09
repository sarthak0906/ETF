import logging
import asyncio
import datetime

from PolygonTickData.PolygonDataAPIConnection import PolgonData
from CalculateETFArbitrage.helper import Helper

class EtfData(object):
    __slots__ = ('symbol', 'data')
    def __init__(self, sybl, dt):
        self.symbol = sybl
        self.data = dt

class CallPolygonApi(object):

    def __init__(self, symbols=None, date=None, previousdate=None, starttime='9:00:00', endtime='17:00:00', endtimeLoop='16:00:00'):
        self.helperObj = Helper()
        self.date = date
        self.starttime = starttime  # 9 AM
        self.endtime = endtime  # 5 PM
        self.endtimeLoop = endtimeLoop  # 4 PM
        self.extractDataTillTime = self.helperObj.stringTimeToDatetime(date=self.date, time=self.endtimeLoop)
        self.marketTimeStamps = self.helperObj.convertStringDateToTS(date=self.date, starttime=self.starttime,endtime=self.endtime)
        self.symbols=symbols

        self.tickHistDataQuotes = None
        self.tickHistDataTrade = None
        self.priceforNAVfilling = None


    async def getDataFromPolygon(self, symbol=None, getMethodForPolygon=None):
        data = getMethodForPolygon(date=self.date, symbol=symbol, endTS=self.marketTimeStamps['marketCloseTS'],limitresult=str(50000))
        lastUnixTimeStamp = self.helperObj.getLastTimeStamp(data)
        await asyncio.sleep(0.2)
        # Check for Pagination
        while self.helperObj.checkTimeStampForPagination(lastUnixTimeStamp,self.extractDataTillTime):
            paginatedData = getMethodForPolygon(date=self.date, symbol=symbol, startTS=str(lastUnixTimeStamp),
                                                endTS=self.marketTimeStamps['marketCloseTS'], limitresult=str(50000))
            lastUnixTimeStamp = self.helperObj.getLastTimeStamp(paginatedData)
            data['results'].extend(paginatedData['results'])
            
        dataobject = EtfData(symbol, data)
        del data # Is this required here? - KTZ
        return dataobject

    # Pass here etfdata object
    def assemblePolygonData(self):
        
        tickHistDataQuotes = []
        tickHistDataTrade = []
        priceforNAVfilling = {}

        Polygonobj = PolgonData()
        # Async to get data from Polygon Starts here
        async def main_():
            async def one_iter(semaphore_, symbol):
                async with semaphore_:
                    tickHistDataQuotes.append(await self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricQuotes))
                    tickHistDataTrade.append(await self.getDataFromPolygon(symbol, Polygonobj.PolygonHistoricTrades))
                    opencloseDf = Polygonobj.PolygonDailyOpenClose(date=self.date, symbol=symbol)
                    priceforNAVfilling[symbol] = opencloseDf['open']
            semaphore = asyncio.BoundedSemaphore(3)
            co_routines = [one_iter(semaphore, symbol) for symbol in self.symbols]
            # co_routines = [one_iter(semaphore, symbol) for symbol in ['AAPL','MSFT','XLK']]
            await asyncio.gather(*co_routines)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main_())

    def getETFHistDataQuotes(self):
    	return self.tickHistDataQuotes

    def getETFHistDataQuotes(self):
    	return self.tickHistDataQuotes

    def getpriceforNAVfilling(self):
    	return self.priceforNAVfilling

      
