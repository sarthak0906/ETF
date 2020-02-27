from HoldingsDataScripts.PullHoldingsList import PullHoldingsListClass
from HoldingsDataScripts.DownloadHoldings import DownloadsEtfHoldingsData
from HoldingsDataScripts.DataCleanFeed import PullandCleanData

# Pull ETF list into a dataframe
ETFListDF = PullHoldingsListClass().ReturnetflistDF()

# For each ETF download all holdings and save to DB
for etf in ETFListDF['Symbol'].tolist():
#for etf in ['XLK']:
    # Download Holdings for given ETF
    DownloadsEtfHoldingsData().fetchHoldingsofETF(etf)

    # Save Holdings for given ETF to DB
    PullandCleanData().readfilesandclean(etf, ETFListDF)