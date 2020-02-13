from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import itertools
import time
# from MongoDB.DownloadHoldings import DownloadsEtfHoldingsData

from MongoDB.Save523TickersListtoDB import ETFListSaver


class masterclass:

    def initialisewebdriver(self,
                            savingpath="/home/piyush/Desktop/ETF10-02-2020/ETFAnalysis/ETFDailyData/ETFTickersDescription/" + datetime.now().strftime(
                                "%Y%m%d")):
        # initialise driver with headless options

        self.chrome_options = webdriver.ChromeOptions()
        self.prefs = {'download.default_directory': savingpath}
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(
            executable_path='/home/piyush/Desktop/ETF10-02-2020/ETFAnalysis/chromextension/chromedriver',
            chrome_options=self.chrome_options)

    def logintoetfdb(self):
        self.driver.get("https://etfdb.com/members/login/")
        e = self.driver.find_element(By.ID, "user_login")
        e.send_keys("karansharmav")
        e = self.driver.find_element(By.ID, "password")
        e.send_keys("etfapp2020")
        e = self.driver.find_element(By.ID, "login-button")
        time.sleep(3)
        e.click()
        self.executor_url = self.driver.command_executor._url
        self.session_id = self.driver.session_id

    def save523tickerslisttodb(self):
        etflistsaverobject = ETFListSaver()
        try:
            etflistsaverobject.readandclean()
            etflistsaverobject.pushtodb()
        except:
            pass

    # def saveholdingstodb(self):
    #     DataCle
