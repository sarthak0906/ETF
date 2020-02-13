from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import itertools
import time
from MongoDB.CallFunctionsFile import masterclass

class Download523TickersList(masterclass):

    def fetchTickerDataDescription(self):
        # initialise driver and login to ETFdb
        super().initialisewebdriver()
        super().logintoetfdb()
        # Fetch Data
        url = 'https://etfdb.com/etfs/sector/'
        self.driver.get(url)
        time.sleep(5)
        e = self.driver.find_element_by_link_text('Export this data to a CSV file')
        time.sleep(10)
        e.click()
        time.sleep(5)
        self.driver.quit()