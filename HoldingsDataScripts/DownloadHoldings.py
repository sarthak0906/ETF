from CommonServices.WebdriverServices import masterclass
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
from selenium.common.exceptions import TimeoutException

path = os.path.join(os.getcwd(), "Logs/HoldingsScraperLogs/")

if not os.path.exists(path):
    os.makedirs(path)
filename = path + datetime.now().strftime("%Y%m%d") + "-HoldingsDataLogs.log"
handler = logging.FileHandler(filename)
logging.basicConfig(filename=filename, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(handler)

from ETFsList_Scripts.List523ETFsMongo import ETFListDocument
from HoldingsDataScripts.ETFMongo import ETF

class PullHoldingsListClass(object):

    def __init__(self, dateofdownload=datetime.now().date()):
        connect('ETF_db', alias='ETF_db')
        self.todaysdata = ETFListDocument.objects(Download_date=dateofdownload).first()
        self.etfdescdf = pd.DataFrame(self.todaysdata.to_mongo().to_dict()['etflist'])

    def ReturnetflistDF(self):
        return self.etfdescdf

    def checkFundHoldingsDate(self, checkDate, etfname):
        if ETF.objects(FundHoldingsDate=datetime.strptime(checkDate, "%Y-%m-%d"), ETFTicker=etfname).first():
            return True
        else:
            return False

class DownloadsEtfHoldingsData(masterclass):

    def fetchHoldingsofETF(self, etfname):
        retries = 0  # login module for all etfs gets zero retries upon failure
        while retries >= 0:
            try:
                # initialise driver and login to ETFdb
                super().initialisewebdriver(
                    savingpath="ETFDailyData/" + datetime.now().strftime(
                        "%Y%m%d"))
                super().logintoetfdb()
                retries = -1
            except TimeoutException:
                retries -= 1
            except Exception as e:
                print(e)
                pass

        # Presence-of-elem-check for all etfs gets zero retries upon failure
        try:
            # get the etf name and request ETFdb page for the same
            url = 'https://etfdb.com/etf/%s/#holdings' % etfname
            self.driver.get(url)
            time.sleep(2)  # wait for page to load
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')))
        except TimeoutException:
            print("Timeout on EC, Retrying once more")
            pass
        except Exception as e:
            print(e)
            pass

        retries = 1  # Check for presence of records and downloading csv for all etfs get only one retry upon failure
        while retries >= 0:
            try:
                # DateCheck receives Boolean that marks presence of record in MongoDB
                # Can/Shall be used to send flag to DataCleanFeed
                DateUpdateElem = self.driver.find_element_by_class_name('date-modified').get_attribute('datetime')
                DateCheck = PullHoldingsListClass().checkFundHoldingsDate(DateUpdateElem, etfname)
                if not DateCheck:
                    el = self.driver.find_element_by_xpath(
                        '//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')
                    el.click()  # clicks download button
                    time.sleep(3)
                else:
                    logger.error("Record for {} already present, Moving to next etf".format(etfname))
                self.driver.quit()
                # if successfully downloaded or data already exists, no retries needed
                retries = -1
                return DateCheck
            except Exception as e:
                print("Exception in DownloadHolding.py for {}".format(etfname))
                print(e)
                logger.exception("Exception in DownloadHolding.py")
                logger.info("Retrying once more")
                retries -= 1
                self.driver.quit()
                # send email on every failure
                EmailSender(['piyush888@gmail.com', 'kshitizsharmav@gmail.com'], 'Exception in DownloadHoldings.py',
                            e).sendemail()
                pass
