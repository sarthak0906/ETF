def getOpenCloseData(self,openCloseURLs=None):
	responses=IOBoundThreading(openCloseURLs)
	priceforNAVfilling={}
	for response in responses:
		priceforNAVfilling[response['symbol']] = response['open']
	return priceforNAVfilling
