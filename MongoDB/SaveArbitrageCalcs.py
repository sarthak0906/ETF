import datetime
from MongoDB.Schemas import arbitragecollection, arbitrage_per_min


class SaveCalculatedArbitrage():
    def insertIntoCollection(self, ETFName=None, dateOfAnalysis=None, data=None, dateWhenAnalysisRan=None):
        print("Saving {} etf into DB...".format(ETFName))
        inserData = {'ETFName': ETFName,
                     'dateOfAnalysis': dateOfAnalysis,
                     'dateWhenAnalysisRan': dateWhenAnalysisRan,
                     'data': data
                     }
        arbitragecollection.insert_one(inserData)

    def  insertIntoPerMinCollection(self, DateTimeOfArbitrage=None, ETFName=None, Arbitrage=None,
                                   Spread=None):
        print("Saving {} etf into Arbitrage Per Min Collection...".format(ETFName))
        inserData = {'DateTimeOfArbitrage': DateTimeOfArbitrage,
                     'ETFName': ETFName,
                     'Arbitrage': Arbitrage,
                     'Spread': Spread
                     }
        arbitrage_per_min.insert_one(inserData)
