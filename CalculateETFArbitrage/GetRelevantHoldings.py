import sys  # Remove in production - KTZ
sys.path.append("..")  # Remove in production - KTZ

from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
from ETFsList_Scripts.List523ETFsMongo import ETFListDocument
from mongoengine import *
class RelevantHoldings():
    def __init__(self):
        self.listofetfs = []
        self.SetOfHoldings = set()
    def getAllETFNames(self):
        try:
            # connect('ETF_db', alias='ETF_db')
            # Connecting to ETF_db on AWS EC2 Production Server
            connect('ETF_db', alias='ETF_db', host='52.91.26.227', port=27017)
            etflistdocument = ETFListDocument.objects().first()
            print(etflistdocument)
            for etf in etflistdocument.etflist:
                self.listofetfs.append(str(etf.Symbol))
            print(self.listofetfs)
        except Exception as e:
            print("Can't Fetch Fund Holdings Data for all ETFs")
            print(e)

    def getAllHoldingsFromAllETFs(self):
        self.getAllETFNames()
        for etf in self.listofetfs:
            try:
                listofholding = LoadHoldingsdata().getHoldingsDataForAllETFfromDB(etf)
                self.SetOfHoldings = self.SetOfHoldings.union(set(listofholding))
            except:
                print("Exception in {} etf".format(etf))
                continue
        return self.SetOfHoldings

if __name__ == "__main__":
    RelevantHoldings().getAllETFNames()