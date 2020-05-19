from mongoengine import connect
import datetime

def fetchETFsWithSameIssuer(connection, date, Issuer=None):
	CollectionName = connection.ETF_db.ETFHoldings
	query={'Issuer':Issuer}
	dataD = CollectionName.find(query,{'FundHoldingsDate':1,'ETFTicker':1,'_id':0}).sort('-FundHoldingsDate')
	# Search How to loop over mongo cursor and extract data - Do Something
	combineddata=[]
	for item in dataD:
		combineddata.append(item['ETFTicker'])
        
	return list(set(combineddata))
