from selenium import webdriver

# I THINK NONE OF THE FOLLOWING IMPORTS ARE NEEDED
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


import time
from ETFsList_Scripts.WebdriverServices import masterclass

class Download523TickersList(masterclass):

    def fetchTickerDataDescription(self):
        # initialise driver and login to ETFdb
        try:
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
        except:
            pass
