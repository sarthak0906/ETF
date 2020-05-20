import schedule

from MongoDB.PerMinDataOperations import PerMinDataOperations
import datetime, time
import pandas as pd



def main():
    start = time.time()
    ########################################################################

    cursor = PerMinDataOperations().FetchPerMinArbitrageFullDay("XLK")
    data = []
    [data.append({'Timestamp': item['Timestamp'], 'Symbol': item['ArbitrageData'][0]['Symbol'],
                  'Arbitrage': item['ArbitrageData'][0]['Arbitrage'], 'Spread': item['ArbitrageData'][0]['Spread']}) for
     item in cursor]
    print("Full Day data for ETF - 'XLK': ")
    print(pd.DataFrame.from_records(data))
    print("#########################################################")
    ########################################################################

    cursor1 = PerMinDataOperations().FetchPerMinLiveData("XLK")
    cursor2 = PerMinDataOperations().FetchPerMinLiveData()

    print("Results for one ETF -- 'XLK' : ")
    data1 = []
    [data1.append({'Timestamp': item['Timestamp'], 'Symbol': item['ArbitrageData'][0]['Symbol'],
                  'Arbitrage': item['ArbitrageData'][0]['Arbitrage'], 'Spread': item['ArbitrageData'][0]['Spread']}) for
     item in cursor1]
    print(pd.DataFrame.from_records(data1))

    print("Results for all ETFs  : ")
    data2 = []
    [data2.extend(item['ArbitrageData']) for item in cursor2]
    print(pd.DataFrame.from_records(data2))
    print("***************************************************************************************")
    end = time.time()
    print("Done in {} seconds".format(end-start))

schedule.every().minute.at(":15").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)