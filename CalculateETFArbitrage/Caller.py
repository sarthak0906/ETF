import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
from datetime import datetime
from CalculateETFArbitrage.Control import ArbitrageCalculation
from MongoDB.SaveArbitrageCalcs import SaveCalculatedArbitrage

try:
    etflist = ['XLY', 'XLC', 'VCR', 'ITB', 'IYC', 'FDIS', 'XRT', 'FXD', 'CHIQ', 'ESPO', 'RTH', 'HERO', 'INCO',
               'VMOT',
               'RCD', 'PEJ', 'JHMC', 'PBS', 'NAIL', 'ONLN', 'BFIT', 'BJK', 'UCC', 'PEZ', 'CARZ', 'PSCD', 'IEDI']
    date = '2020-03-16'
    for etfname in etflist:
        data = ArbitrageCalculation().calculateArbitrage(etfname, date)
        SaveCalculatedArbitrage().insertIntoCollection(etfname, datetime.now().date().strftime('%Y-%m-%d'),
                                                       data.to_dict(orient='records'))
except Exception as e:
    print("exception in {} etf".format(etfname))
    print(e)

