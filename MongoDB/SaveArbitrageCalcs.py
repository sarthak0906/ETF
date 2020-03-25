import datetime
from MongoDB.Schemas import arbitragecollection

class SaveCalculatedArbitrage():
    def insertIntoCollection(self, ETFName=None, dateOfAnalysis=None, data=None):
        print("Saving {} etf into DB...".format(ETFName))
        inserData = {'ETFName': ETFName,
                     'dateOfAnalysis': datetime.datetime.strptime(dateOfAnalysis, '%Y-%m-%d'),
                     'data': data
                     }
        arbitragecollection.insert_one(inserData)