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
        # todaysdata = ETFListDocument.objects(Download_date=datetime.now().date()).first()
        # etflist = todaysdata.etflist
        # # print(todaysdata.to_mongo().to_dict()['etflist'])
        # # print(pd.DataFrame(todaysdata.to_mongo().to_dict()['etflist']))
        super().initialisewebdriver(
            savingpath="ETFDailyData/" + datetime.now().strftime(
                "%Y%m%d"))
        super().logintoetfdb()
        # Fetch Data
        # for doc in etflist:
        #     try:
        #         url = 'https://etfdb.com/etf/%s/#holdings' % doc.Symbol
        #         self.driver.get(url)
        #         time.sleep(3)
        #         e = self.driver.find_element_by_xpath(
        #             '//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')
        #         e.click()
        #     except Exception as e:
        #         print("Downloading Data for following ticker failed =" + doc.Symbol)
        #         print(e)
        #         continue

        url = 'https://etfdb.com/etf/%s/#holdings' % etfname
        # url = 'https://etfdb.com/etf/XLK/#holdings'
        self.driver.get(url)
        time.sleep(3)
        e = self.driver.find_element_by_xpath(
            '//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')
        e.click()
        self.driver.close()
