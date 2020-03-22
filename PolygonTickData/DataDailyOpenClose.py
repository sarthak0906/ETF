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

	def getOpenCloseData(self,openCloseURLs=None):
		responses=IOBoundThreading(openCloseURLs)
		priceforNAVfilling={}
		for response in responses:
			print(response)
			priceforNAVfilling[response['symbol']] = response['open']
		return priceforNAVfilling

	def run(self):
		return self.getOpenCloseData(openCloseURLs=self.createUrls())