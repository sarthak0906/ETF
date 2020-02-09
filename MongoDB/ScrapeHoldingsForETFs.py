from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import itertools
import time

class DownloadsEtfHoldingsData(object):
    
    def __init__(self,savingpath):
        self.savingpath = savingpath
        self.chrome_options = webdriver.ChromeOptions()
        self.prefs = {'download.default_directory' : self.savingpath,'behavior': 'allow'}
        '''
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1440, 900")
        self.chrome_options.add_argument("no-sandbox");
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        '''
        try:
            self.driver = webdriver.Chrome(executable_path='../chromextensionlinux/chromedriver',chrome_options=self.chrome_options)
        except:
            self.driver = webdriver.Chrome(executable_path='../chromextensionMAC/chromedriver',chrome_options=self.chrome_options)
        
    def loginToEtfDb(self):
        self.driver.get("https://etfdb.com/members/login/")
        e = self.driver.find_element(By.ID, "user_login")
        e.send_keys("karansharmav")
        e = self.driver.find_element(By.ID, "password")
        e.send_keys("etfapp2020")
        e = self.driver.find_element(By.ID, "login-button") 
        time.sleep(3)
        e.click()
        
    def fetchDataForEtfTicker(self,ticker):
        # Fetch Data
        url='https://etfdb.com/etf/%s/#holdings'% (ticker)
        self.driver.get(url)
        time.sleep(4)
        e = self.driver.find_element_by_xpath('//input[@type="submit" and @value="Download Detailed ETF Holdings and Analytics"]')
        e.click()
    
    def closedriver(self):
        self.driver.close()


if __name__ == "__main__":

    ETFTickerList=pd.read_csv("../ETFDailyData/ETFTickersDecription/"+datetime.now().strftime("%Y%m%d")+"/etfs_details_type_fund_flow.csv",index_col='Symbol')
    tickers=ETFTickerList.index.tolist()

    savingpath='../ETFDailyData'+'/'+datetime.now().strftime("%Y%m%d")
    ob=DownloadsEtfHoldingsData(savingpath)
    ob.loginToEtfDb()
    for i in tickers:
        try:
            print("Downloading Holdings Data For = " + i)
            ob.fetchDataForEtfTicker(i)
        except Exception as e:
            print("!!!!!!!!!!Warning!!!!!!!!!!!!!")
            print("Downloading Data for following ticker Failed = " + i)
            print(e)
            continue
    ob.closedriver()



