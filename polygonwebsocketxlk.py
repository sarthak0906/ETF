import time
from mongoengine import *
from datetime import datetime
from polygon import WebSocketClient, STOCKS_CLUSTER
from HoldingsDataScripts.ETFMongo import ETF
import pandas as pd

def get_tickers_list():
    connect('ETF_db', alias='ETF_db')
    etfs = ETF.objects(ETFTicker='XLK').first()
    print(etfs.to_mongo().to_dict()['holdings'])
    holdings = pd.DataFrame(etfs.to_mongo().to_dict()['holdings'])
    holdings_list = holdings['TickerSymbol'].tolist()
    return holdings_list

def my_custom_process_message(message):
    print("this is my custom message processing", message)


def my_custom_error_handler(ws, error):
    print("this is my custom error handler", error)


def my_custom_close_handler(ws):
    print("this is my custom close handler")


def main():
    key = 'M_PKVL_rqHZI7VM9ZYO_hwPiConz5rIklx893F'
    my_client = WebSocketClient(STOCKS_CLUSTER, key, my_custom_process_message)
    my_client.run_async()
    tickerlist = get_tickers_list()
    ticker_list = ["T."+str(x) for x in tickerlist]
    print(ticker_list)
    my_client.subscribe(*ticker_list)
    time.sleep(1)

    my_client.close_connection()


if __name__ == "__main__":
    main()