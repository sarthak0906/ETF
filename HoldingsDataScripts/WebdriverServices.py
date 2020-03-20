import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from EmailNotifier import SendEmail

class masterclass:

    def initialisewebdriver(self, savingpath='ETFDailyData/ETFTickersDescription/'+datetime.now().strftime("%Y%m%d")):
        # initialise driver with headless options

        # Getting the absolute path for the passed savingpath
        self.savingpath = os.path.join(os.getcwd(), savingpath)
        self.chrome_options = Options()
        # specifying default download directory for the particular instance of ChromeDriver
        self.prefs = {'download.default_directory': self.savingpath}
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.binary_location = "/usr/bin/google-chrome-stable"
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(executable_path='./chromextension/chromedriverWin/chromedriver', chrome_options=self.chrome_options)

    def logintoetfdb(self):
        self.driver.get("https://etfdb.com/members/login/")
        # wait only until the presence of 'login-button' is detected
        element = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "login-button")))
        e = self.driver.find_element(By.ID, "user_login")
        e.send_keys("piyushg795")
        e = self.driver.find_element(By.ID, "password")
        e.send_keys("etfapp2020")
        e = self.driver.find_element(By.ID, "login-button")
        e.click()

