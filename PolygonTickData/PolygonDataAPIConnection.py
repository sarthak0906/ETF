import requests
from datetime import datetime


class PolgonData(object):

	def __init__(self):
		self.params=params = (('apiKey', 'M_PKVL_rqHZI7VM9ZYO_hwPiConz5rIklx893F'),)
		
	def PolygonLastTrades(self,symbol):
		# Make use of Tickers
		requesturl='https://api.polygon.io/v1/last/stocks/'+symbol
		response = requests.get(requesturl, params=self.params)
		return response

	def PolygonHistoricTrades(self, symbol=None,date=datetime.today().date().strftime('%Y-%m-%d'), limit=10):
		# Make use of Tickers, Date and Limit
		requesturl='https://api.polygon.io/v2/ticks/stocks/trades/AAPL/2018-02-02?limit=10'
		response = requests.get('', params=self.params)
		return response
	
	def PolygonTickTrades(self,symbolList=None):
		requesturl="wss://api.polygon.io/v1/last/stocks/"
		def on_message(ws, message):
			print(message)

		def on_error(ws, error):
			print(error)

		def on_close(ws):
			print("### closed ###")

		def on_open(ws):
			ws.send('{"action":"auth","params":"M_PKVL_rqHZI7VM9ZYO_hwPiConz5rIklx893F"}')
			#!!!! replace by symbolList later
			ws.send('{"action":"subscribe","params":"T.MSFT", "T.AAPL", "T.AMD", "T.NVDA"}')

		def runLiveTickData(self):
			websocket.enableTrace(True)
			ws = websocket.WebSocketApp(requesturl,
									  on_message = on_message,
									  on_error = on_error,
									  on_close = on_close)
			ws.on_open = on_open
			ws.run_forever()    


