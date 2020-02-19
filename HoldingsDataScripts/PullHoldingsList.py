from mongoengine import *
import pandas as pd
import os
from datetime import datetime

from ETFsList_Scripts.List523ETFsMongo import ETFListDocument
from ETFsList_Scripts.ETFListCollection import ETFListData




class PullHoldingsListClass(object):

    def __init__(self, dateofdownload=datetime.now().date()):
        connect('ETF_db', alias='ETF_db')
        self.todaysdata = ETFListDocument.objects(Download_date=dateofdownload).first()
        self.etfdescdf = pd.DataFrame(self.todaysdata.to_mongo().to_dict()['etflist'])

    def ReturnetflistDF(self):
        return self.etfdescdf
