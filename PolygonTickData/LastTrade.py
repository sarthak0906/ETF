import requests
from datetime import datetime


class PolgonData(object):

	def __init__(self,tickers=[]):
		self.params=params = (('apiKey', 'M_PKVL_rqHZI7VM9ZYO_hwPiConz5rIklx893F'))
		self.tickers=tickers
	
	def PolygonLastTrade(self):
		# Make use of Tickers
		requesturl='https://api.polygon.io/v1/last/stocks/AAPL'
		response = requests.get(requesturl, params=self.params)
		return response.text

	def PolygonHistoricTrades(self, date=datetime.today().date().strftime('%Y-%m-%d'), limit=10):
		# Make use of Tickers, Date and Limit
		requesturl='https://api.polygon.io/v2/ticks/stocks/trades/AAPL/2018-02-02?limit=10'
		response = requests.get('', params=self.params)
		return response.text


if __name__== "__main__":
	# Last Trade for a symbol
	ob=PolgonData(tickets=['AAPL','MSFT','TSLA'])
	
	# Historic Quotes
	




#response = requests.get('https://api.polygon.io/v1/last/stocks/AAPL', params=params)