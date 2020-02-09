from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import itertools
import time

from ETFDBWebscrapper import DownloadsEtfHoldingsData

class ETFTickerDescription(DownloadsEtfHoldingsData):
    
    def __init__(self,savingpath):
        super(ETFTickerDescription,self).__init__(savingpath)

    def fetchTickerDataDescription(self):
        # Fetch Data
        url='https://etfdb.com/etfs/sector/'
        self.driver.get(url)
        time.sleep(2)
        e = self.driver.find_element_by_link_text('Export this data to a CSV file')
        time.sleep(5)
        e.click()
        time.sleep(10)
    

if __name__ == "__main__":

    savingpath='../ETFDailyData'+'/'+'ETFTIckersDecription'+'/'+datetime.now().strftime("%Y%m%d")
    ob=ETFTickerDescription(savingpath)
    ob.loginToEtfDb()
    ob.fetchTickerDataDescription()
    ob.closedriver()



