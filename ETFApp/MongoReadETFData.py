from pymongo import MongoClient
from datetime import datetime
import pandas as pd

class RetrieveData(object):

	def __init__(self):
		self.client=MongoClient('localhost', 27017)
		self.db=self.client.ETF_db
		self.collection = self.db['ETFHoldings']

	def buildQuery(self):
		query={'FundHoldings_date':datetime(2020,2,7)}
	
	def queryData(self,query):
		return pd.DataFrame.from_dict(self.collection.find(query))
