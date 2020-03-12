# Add paths to System PATH for the packages to be locatable by python
import sys

sys.path.extend(['/home/piyush/Desktop/etf/ETFAnalysis', '/home/piyush/Desktop/etf/ETFAnalysis/ETFsList_Scripts',
                 '/home/piyush/Desktop/etf/ETFAnalysis/HoldingsDataScripts',
                 '/home/piyush/Desktop/etf/ETFAnalysis/CommonServices'])
sys.path.extend(['/home/ubuntu/ETFAnalysis', '/home/ubuntu/ETFAnalysis/ETFsList_Scripts',
                 '/home/ubuntu/ETFAnalysis/HoldingsDataScripts', '/home/ubuntu/ETFAnalysis/CommonServices'])
# Use absolute import paths
import ETFsList_Scripts.WebdriverServices as serv
from ETFsList_Scripts.Download523TickersList import Download523TickersList
from HoldingsDataScripts.DownloadHoldings import DownloadsEtfHoldingsData, PullHoldingsListClass
from HoldingsDataScripts.DataCleanFeed import PullandCleanData
from datetime import datetime
from CommonServices.EmailService import EmailSender
from CommonServices.DirectoryRemover import Directory_Remover
import getpass
import logging

filename = datetime.now().strftime("%Y%m%d") + "-HoldingsDataLogs.log"
logging.basicConfig(filename=filename, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def startCronJobForETFHoldings():
    Download523TickersList().fetchTickerDataDescription()
    serv.masterclass().savelisttodb()
    # Pull ETF list into a dataframe
    ETFListDF = PullHoldingsListClass().ReturnetflistDF()

    # For each ETF download all holdings and save to DB
    for etf in ETFListDF['Symbol'].tolist():
        # for etf in ['XLK']:
        # Download Holdings for given ETF
        DownloadsEtfHoldingsData().fetchHoldingsofETF(etf)

        # Save Holdings for given ETF to DB
        PullandCleanData().readfilesandclean(etf, ETFListDF)


try:
    startCronJobForETFHoldings()
    # Begin deletion process after storing to DB is finished
    # Check for system via username of the system
    username = getpass.getuser()
    # Delete both 523 ETF List CSV file and Downloaded Ticker CSV files
    if username is 'piyush':
        Directory_Remover('/home/piyush/Desktop/etfnew/ETFAnalysis/ETFDailyData').remdir()
    else:
        Directory_Remover('/home/ubuntu/ETFAnalysis/ETFDailyData').remdir()
except Exception as e:
    print(e)
    logger.exception("Exception in ProcessCaller")
    # receivers' address in a list (1 or more addresses), subject, body - exception message
    EmailSender(['piyush888@gmail.com', 'kshitizsharmav@gmail.com'], 'Exception Occurred', e).sendemail()
    pass
