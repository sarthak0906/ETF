import ETFsList_Scripts.WebdriverServices as serv
from ETFsList_Scripts.Download523TickersList import Download523TickersList

Download523TickersList().fetchTickerDataDescription()
serv.masterclass().savelisttodb()
