from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
from ETFsList_Scripts.WebdriverServices import masterclass

class Download523TickersList(masterclass):

    def fetchTickerDataDescription(self):
        # initialise driver and login to ETFdb
        try:
            super().initialisewebdriver()
            super().logintoetfdb()
            # Fetch List using this url
            url = 'https://etfdb.com/etfs/sector/'
            self.driver.get(url)
            element = WebDriverWait(self.driver, 180).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Export this data to a CSV file")))
            e = self.driver.find_element_by_link_text('Export this data to a CSV file')
            e.click()
            time.sleep(3)
            self.driver.quit()
        except:
            pass
