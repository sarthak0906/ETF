from HoldingsDataScripts.WebdriverServices import masterclass
from mongoengine import *
import pandas as pd
from datetime import datetime
import logging
import time

logging.basicConfig(filename="HoldingsDataLogs.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from ETFsList_Scripts.List523ETFsMongo import ETFListDocument

class PullHoldingsListClass(object):

    def __init__(self, dateofdownload=datetime.now().date()):
        connect('ETF_db', alias='ETF_db')
        self.todaysdata = ETFListDocument.objects(Download_date=dateofdownload).first()
        self.etfdescdf = pd.DataFrame(self.todaysdata.to_mongo().to_dict()['etflist'])

    def ReturnetflistDF(self):
        return self.etfdescdf

class DownloadsEtfHoldingsData(masterclass):

    def fetchHoldingsofETF(self, etfname):
        retries = 1
        while retries >= 0:
            try:
                # initialise driver and login to ETFdb
                super().initialisewebdriver(
                    savingpath="ETFDailyData/" + datetime.now().strftime(
                        "%Y%m%d"))
                super().logintoetfdb()

                url = 'https://etfdb.com/etf/%s/#holdings' % etfname
                self.driver.get(url)
                time.sleep(2)
                e = self.driver.find_element_by_xpath(
                    '//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')
                e.click()
                self.driver.close()
                retries = -1
            except Exception as e:
                print("Exception in DownloadHolding.py for {}".format(etfname))
                print(e)
                logger.exception("Exception in DownloadHolding.py")
                logger.info("Retrying once more")
                retries -= 1
                pass
