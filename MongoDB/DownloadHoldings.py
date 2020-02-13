from datetime import datetime
import pandas as pd
import itertools
import time
import mongoengine
from MongoDB.CallFunctionsFile import masterclass
from MongoDB.List523ETFsMongo import ETFListDocument
from MongoDB.ETFListCollection import ETFListData


class DownloadsEtfHoldingsData(masterclass):

    def fetchDataForEtfTicker(self):
        # initialise driver and login to ETFdb
        todaysdata = ETFListDocument.objects(Download_date=datetime.now().date()).first()
        etflist = todaysdata.etflist
        # print(todaysdata.to_mongo().to_dict()['etflist'])
        # print(pd.DataFrame(todaysdata.to_mongo().to_dict()['etflist']))
        super().initialisewebdriver(
            savingpath="/home/piyush/Desktop/ETF10-02-2020/ETFAnalysis/ETFDailyData/" + datetime.now().strftime(
                "%Y%m%d"))
        super().logintoetfdb()
        # Fetch Data
        for doc in etflist:
            try:
                url = 'https://etfdb.com/etf/%s/#holdings' % doc.Symbol
                self.driver.get(url)
                time.sleep(3)
                e = self.driver.find_element_by_xpath(
                    '//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')
                e.click()
            except Exception as e:
                print("Downloading Data for following ticker failed =" + doc.Symbol)
                print(e)
                continue
        self.driver.close()
