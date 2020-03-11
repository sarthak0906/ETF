import sys

sys.path.extend(['/home/piyush/Desktop/etf/ETFAnalysis', '/home/piyush/Desktop/etf/ETFAnalysis/ETFsList_Scripts',
                 '/home/piyush/Desktop/etf/ETFAnalysis/HoldingsDataScripts'])
sys.path.extend(['/home/ubuntu/ETFAnalysis', '/home/ubuntu/ETFAnalysis/ETFsList_Scripts',
                 '/home/ubuntu/ETFAnalysis/HoldingsDataScripts'])

import ETFsList_Scripts.WebdriverServices as serv
from ETFsList_Scripts.Download523TickersList import Download523TickersList
from HoldingsDataScripts.DownloadHoldings import DownloadsEtfHoldingsData, PullHoldingsListClass
from HoldingsDataScripts.DataCleanFeed import PullandCleanData
import asyncio

import logging

logging.basicConfig(filename="HoldingsDataLogs.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def startCronJobForETFHoldings():
    Download523TickersList().fetchTickerDataDescription()
    serv.masterclass().savelisttodb()
    # Pull ETF list into a dataframe
    ETFListDF = PullHoldingsListClass().ReturnetflistDF()

    # For each ETF download all holdings and save to DB
    for etf in ETFListDF['Symbol'].tolist():
        # for etf in ['XLK']:
        # Download Holdings for given ETF
        DownloadsEtfHoldingsData().fetchHoldingsofETF(etf)

        # Save Holdings for given ETF to DB
        PullandCleanData().readfilesandclean(etf, ETFListDF)


    #######################################################################################################################

    # async def main():
    #     async def one_iteration(semaphore_, etf):
    #         async with semaphore_:
    #             await DownloadsEtfHoldingsData().fetchHoldingsofETF(etf)
    #             await PullandCleanData().readfilesandclean(etf, ETFListDF)
    #
    #     semaphore = asyncio.BoundedSemaphore(2)
    #     co_routines = [one_iteration(semaphore, etf) for etf in ETFListDF['Symbol'].tolist()]
    #     # co_routines = [one_iteration(semaphore, etf) for etf in ['XLK','XLV','QQQ','VGT','IYW','IGV','FTEC','IXN']]
    #     await asyncio.gather(*co_routines)

    #######################################################################################################################

    # async def main_():
    #     async def one_iter(semaphore_, etf):
    #         async with semaphore_:
    #             await DownloadsEtfHoldingsData().fetchHoldingsofETF(etf)
    #             PullandCleanData().readfilesandclean(etf, ETFListDF)
    #
    #     semaphore = asyncio.BoundedSemaphore(2)
    #     # co_routines = [one_iter(semaphore, etf) for etf in ETFListDF['Symbol'].tolist()]
    #     co_routines = [one_iter(semaphore, etf) for etf in ['SGDM','XLK','BDCS','IYW']]
    #     await asyncio.gather(*co_routines)
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main_())


try:
    startCronJobForETFHoldings()
except Exception as e:
    print(e)
    logger.exception("Exception in ProcessCaller")
