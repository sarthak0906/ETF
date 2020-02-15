# Install these packages
# pip install websocket-client

import websocket

def on_message(ws, message):
	print(message)

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed ###")

def on_open(ws):
	ws.send('{"action":"auth","params":"M_PKVL_rqHZI7VM9ZYO_hwPiConz5rIklx893F"}')
	ws.send('{"action":"subscribe","params":"T.MSFT", "T.AAPL", "T.AMD", "T.NVDA"}')

if __name__ == "__main__":
	#https://api.polygon.io/v1/last/stoc#ks/AAPL?apiKey=M_PKVL_rqHZI7VM9ZYO_hwPiConz5rIklx893F
	websocket.enableTrace(True)
	#https://api.polygon.io/v1/last/stocks/
	
	ws = websocket.WebSocketApp("wss://api.polygon.io/v1/last/stocks/",
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close)
	ws.on_open = on_open
	#ws.run_forever()    


