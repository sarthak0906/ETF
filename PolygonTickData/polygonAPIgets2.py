from aiohttp import ClientSession, TCPConnector
import asyncio
import sys
from pypeln.asyncio_task import TaskPool
import json
from CalculateETFArbitrage.helper import Helper
from datetime import datetime

import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ


limit = 10


# async def fetch(url, session):
#     async with session.get(url) as response:
#         return await response.read()


async def PolygonHistoricTrades(session, date=None, symbol=None, startTS=None, endTS=None, limitresult=10):
    params = (('apiKey', 'M_PKVL_rqHZI7VM9ZYO_hwPiConz5rIklx893F'),)
    if startTS <= Helper().stringTimeToDatetime(date=date, time='9:30:00'):
        requesturl = 'https://api.polygon.io/v2/ticks/stocks/trades/' + symbol + '/' + date + '?timestampLimit=' + Helper().unix_time_millis(
            endTS) + '&limit=' + str(limitresult)
        print("First Request For = " + symbol)
    else:
        # For Getting Paginated Request
        requesturl = 'https://api.polygon.io/v2/ticks/stocks/trades/' + symbol + '/' + date + '?timestamp=' + Helper().unix_time_millis(
            startTS) + '&timestampLimit=' + Helper().unix_time_millis(endTS) + '&limit=' + str(limitresult)
        print("Paginated Request For = " + symbol)

    async with session.get(requesturl, params=params) as response:
        return await json.loads(response.text())


async def _main(loop):
    symbol = 'XLK'
    date = "2020-03-02"
    startts = Helper().stringTimeToDatetime(date=date, time='9:30:00')
    endts = Helper().stringTimeToDatetime(date=date, time='16:00:00')
    async with ClientSession() as session, TaskPool(limit, loop) as tasks:
        while startts <= endts:
            data = await tasks.put(
                PolygonHistoricTrades(session=session, date=date, symbol=symbol, startTS=startts, endTS=endts,
                                      limitresult=50000))
            startts = int(data['results'][-1]['t'])
            print(startts)


loop = asyncio.get_event_loop()
loop.run_until_complete(_main(loop))
