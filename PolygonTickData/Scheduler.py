import sched, time
from PolygonDataAPIConnection import PolgonData
import logging

class ScheduleDataCallFromPolygon(object):

	def __init__(self,tickerlist=None,methodtoCall=None):
		self.tickerlist=tickerlist
		self.methodtoCall=methodtoCall
		

	def getDataFromPolygonAPI(self,sc,timedelay): 
		
		for i in self.tickerlist:
			response=self.methodtoCall(i)
			print(response.text)
		sc.enter(timedelay, 1, self.getDataFromPolygonAPI, (sc,timedelay,))

if __name__== "__main__":
	timedelay=2
	sc = sched.scheduler(time.time, time.sleep)
	schedObject=ScheduleDataCallFromPolygon(tickerlist=['AAPL','MSFT','TSLA'],methodtoCall=PolgonData().PolygonLastTrades)
	sc.enter(timedelay, 1, schedObject.getDataFromPolygonAPI, (sc,timedelay,))
	sc.run()
