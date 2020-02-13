import MongoDB.CallFunctionsFile as cf
from MongoDB.Download523TickersList import Download523TickersList
from MongoDB.DownloadHoldings import DownloadsEtfHoldingsData
from MongoDB.DataCleanFeed import PullandCleanData

Download523TickersList().fetchTickerDataDescription()
cf.masterclass().save523tickerslisttodb()
DownloadsEtfHoldingsData().fetchDataForEtfTicker()
PullandCleanData().readfilesandclean()