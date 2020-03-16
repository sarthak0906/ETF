from HoldingsDataScripts.WebdriverServices import masterclass
from mongoengine import *
import pandas as pd
from datetime import datetime
import logging
import time
from CommonServices.EmailService import EmailSender
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os

if not os.path.exists("Logs/HoldingsScraperLogs/"):
    os.makedirs("Logs/HoldingsScraperLogs/")
filename = "/home/ubuntu/ETFAnalysis/Logs/HoldingsScraperLogs/" + datetime.now().strftime("%Y%m%d") + "-HoldingsDataLogs.log"
handler = logging.FileHandler(filename)
logging.basicConfig(filename=filename, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

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
        retries = 1  # all etfs get only one retry upon failure
        while retries >= 0:
            try:
                # initialise driver and login to ETFdb
                super().initialisewebdriver(
                    savingpath="ETFDailyData/" + datetime.now().strftime(
                        "%Y%m%d"))
                super().logintoetfdb()

                # get the etf name and request ETFdb page for the same
                url = 'https://etfdb.com/etf/%s/#holdings' % etfname
                self.driver.get(url)
                time.sleep(2)  # wait for page to load
                e = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')))
                e.click()  # clicks download button
                self.driver.close()
                # if successfully downloaded, no retries needed
                retries = -1
            except Exception as e:
                print("Exception in DownloadHolding.py for {}".format(etfname))
                print(e)
                logger.exception("Exception in DownloadHolding.py")
                logger.info("Retrying once more")
                retries -= 1
                # send email on every failure
                EmailSender(['piyush888@gmail.com', 'kshitizsharmav@gmail.com'], 'Exception in DownloadHoldings.py',
                            e).sendemail()
                pass
