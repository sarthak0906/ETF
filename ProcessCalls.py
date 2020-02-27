import sys
sys.path.extend(['/home/piyush/Desktop/etf/ETFAnalysis', '/home/piyush/Desktop/etf/ETFAnalysis/ETFsList_Scripts', '/home/piyush/Desktop/etf/ETFAnalysis/HoldingsDataScripts'])


import ETFsList_Scripts.WebdriverServices as serv
from ETFsList_Scripts.Download523TickersList import Download523TickersList

from HoldingsDataScripts.PullHoldingsList import PullHoldingsListClass
from HoldingsDataScripts.DownloadHoldings import DownloadsEtfHoldingsData
from HoldingsDataScripts.DataCleanFeed import PullandCleanData


Download523TickersList().fetchTickerDataDescription()
serv.masterclass().save523tickerslisttodb()

# Pull ETF list into a dataframe
ETFListDF = PullHoldingsListClass().ReturnetflistDF()

# For each ETF download all holdings and save to DB
for etf in ETFListDF['Symbol'].tolist():
# for etf in ['XLK']:
    # Download Holdings for given ETF
    DownloadsEtfHoldingsData().fetchHoldingsofETF(etf)

    # Save Holdings for given ETF to DB
    PullandCleanData().readfilesandclean(etf, ETFListDF)