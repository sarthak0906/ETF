import pandas as pd
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
from CalculateETFArbitrage.GetRelevantHoldings import RelevantHoldings
import json
import datetime

workinglist = list(pd.read_csv("/home/piyush/Desktop/etf1903/CalculateETFArbitrage/WorkingETFs.csv").columns.values)
holdingslist = []
etfdicts = []
for etfname in workinglist:
    holdings2 = []
    try:
        df = LoadHoldingsdata().getHoldingsDatafromDB(etfname,
                                                                     (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
                                                                         "%Y-%m-%d"))
        df.drop(columns=['TickerName'], inplace=True)
        df.rename(columns={'TickerSymbol':'symbol', 'TickerWeight':'weight'},inplace=True)
        dfdict = df.to_dict()
        holdingslist.extend(df['symbol'].to_list())
        holdings2.append(dfdict)
        dictetf = {etfname: holdings2}
        etfdicts.append(dictetf)
    except:
        pass

out_file = open("etf-hold.json", "w")
json.dump(etfdicts, out_file, indent=6)
out_file.close()
holdingslist = holdingslist + workinglist
# tickerlist = ["AM." + x for x in holdingslist]
tickerset = set(holdingslist)

RelevantHoldings().write_to_csv(etflist=list(tickerset), filename="tickerlist.csv")
