from mongoengine import connect
import datetime
import pandas as pd

def fetchETFsWithSameIssuer(connection, date, Issuer=None):
	CollectionName = connection.ETF_db.ETFHoldings
	query={'Issuer':Issuer}
	dataD = CollectionName.find(query,{'FundHoldingsDate':1,'ETFTicker':1,'TotalAssetsUnderMgmt':1,'ETFName':1,'_id':0}).sort('-FundHoldingsDate')
	# Search How to loop over mongo cursor and extract data - Do Something
	combineddata={}
	for item in dataD:
		if item['ETFTicker'] not in list(item.keys()):
			combineddata[item['ETFTicker']]={'ETFName':item['ETFName'],
			'TotalAssetsUnderMgmt':item['TotalAssetsUnderMgmt']}
		
	combineddata = pd.DataFrame(combineddata).to_dict(orient='records')
        
	return combineddata
