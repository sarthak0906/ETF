from datetime import datetime
import pandas as pd
import itertools
import time
import mongoengine
from WebdriverServices import masterclass
from ETFsList_Scripts.List523ETFsMongo import ETFListDocument
from ETFsList_Scripts.ETFListCollection import ETFListData


class DownloadsEtfHoldingsData(masterclass):

    def fetchHoldingsofETF(self, etfname):
        # initialise driver and login to ETFdb
        super().initialisewebdriver(
            savingpath="ETFDailyData/" + datetime.now().strftime(
                "%Y%m%d"))
        super().logintoetfdb()

        url = 'https://etfdb.com/etf/%s/#holdings' % etfname
        # url = 'https://etfdb.com/etf/XLK/#holdings'
        self.driver.get(url)
        time.sleep(3)
        e = self.driver.find_element_by_xpath(
            '//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')
        e.click()
        self.driver.close()
