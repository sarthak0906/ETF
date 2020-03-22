import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ

import pandas as pd
import logging
from PolygonTickData.helper import Helper
from CalculateETFArbitrage.LoadEtfHoldings import LoadHoldingsdata
from PolygonTickData.CommonPolygonTradeQuotes import AssembleData
from MongoDB.Schemas import QuotesdataSchema, TradesdataSchema

class ArbitrageAnalysis(object):

	def __init__(self):
		pass

	def runAnalysis(self):
		pass

	def storeAnalysisResults(self):
		pass

