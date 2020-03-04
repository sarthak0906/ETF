import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import itertools
import time


# from EmailNotifier import SendEmail

class masterclass:

    def initialisewebdriver(self, savingpath='ETFDailyData/ETFTickersDescription/'+datetime.now().strftime("%Y%m%d")):
        # initialise driver with headless options
        # self.savingpath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), savingpath)
        self.savingpath = os.path.join(os.getcwd(), savingpath)
        #print(self.savingpath)
        self.chrome_options = webdriver.ChromeOptions()
        self.prefs = {'download.default_directory': self.savingpath}
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(executable_path='./chromextension/chromedriverWin/chromedriver', chrome_options=self.chrome_options)

    def logintoetfdb(self):
        self.driver.get("https://etfdb.com/members/login/")
        e = self.driver.find_element(By.ID, "user_login")
        e.send_keys("ticketsoft")
        e = self.driver.find_element(By.ID, "password")
        e.send_keys("etfapp2020")
        e = self.driver.find_element(By.ID, "login-button")
        time.sleep(3)
        e.click()

