import sys
sys.path.append("..")  # Remove in production - KTZ

from PolygonTickData.PolygonCreateURLS import PolgonDataCreateURLS
from CommonServices.ThreadingRequests import IOBoundThreading

class DailyOpenCloseData(object):

	def __init__(self,symbols=None, date=None):
		self.symbols=symbols
		self.date=date

	def createUrls(self):
		print(PolgonDataCreateURLS().PolygonDailyOpenClose(date=self.date, symbol=symbol) for symbol in self.symbols)
		return [PolgonDataCreateURLS().PolygonDailyOpenClose(date=self.date, symbol=symbol) for symbol in self.symbols]

	# Used for threading
	def getOpenCloseData(self,openCloseURLs=None):
		responses=IOBoundThreading(openCloseURLs)
		priceforNAVfilling={}
		for response in responses:
			print(response)
			try:
				priceforNAVfilling[response['symbol']] = response['open']
			except Exception as e:
				print(e)
				continue

		return priceforNAVfilling

	def run(self):
		return self.getOpenCloseData(openCloseURLs=self.createUrls())

'''
# Debugger Code
	# TO debug where it's failling
	def debuggetOpenCloseData(self,openCloseURLs=None):
		import urllib.request
		import json
		priceforNAVfilling={}
		for url in openCloseURLs:
			print(url)
			response=json.loads(urllib.request.urlopen(url).read())
			print(response)
			priceforNAVfilling[response['symbol']] = response['open']
		return priceforNAVfilling

if __name__=="__main__":
	from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
	etfData=LoadHoldingsdata(etfname='XLK', fundholdingsdate='2020-03-16')
	obj=DailyOpenCloseData(symbols=etfData.getSymbols(), date='2020-03-16')
	obj.debuggetOpenCloseData(openCloseURLs=obj.createUrls())
# Debugger Code
'''