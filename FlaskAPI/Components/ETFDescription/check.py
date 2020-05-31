import sys
import os
sys.path.append("../../../")

from PolygonTickData.HistoricOHLCgetter import HistoricOHLC

ob = HistoricOHLC()
ob.getopenlowhistoric(etfname='XLK', startdate='2010-01-01')