import datetime
from MongoDB.Schemas import arbitragecollection

class SaveCalculatedArbitrage():
    def insertIntoCollection(self, ETFName=None, dateOfAnalysis=None, data=None,dateWhenAnalysisRan=None):
        print("Saving {} etf into DB...".format(ETFName))
        inserData = {'ETFName': ETFName,
                     'dateOfAnalysis':dateOfAnalysis,
                     'dateWhenAnalysisRan':dateWhenAnalysisRan,
                     'data': data
                     }
        arbitragecollection.insert_one(inserData)