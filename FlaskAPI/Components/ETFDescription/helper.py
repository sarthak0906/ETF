from mongoengine import connect
import datetime


def fetchETFsWithSameIssuer(connection, date, Issuer=None):
    CollectionName = connection.ETF_db.ETFHoldings
    query = {'Issuer': Issuer}
    dataD = CollectionName.find(query, {'FundHoldingsDate': 1, 'ETFTicker': 1, 'TotalAssetsUnderMgmt': 1, 'ETFName': 1,
                                        '_id': 0}).sort('-FundHoldingsDate')
    # Search How to loop over mongo cursor and extract data - Do Something
    combineddata = {}
    for item in dataD:
        if item['ETFTicker'] not in list(item.keys()):
            combineddata[item['ETFTicker']] = {'ETFName': item['ETFName'],
                                               'TotalAssetsUnderMgmt': item['TotalAssetsUnderMgmt']}

    return combineddata


def fetchETFsWithSameETFdbCategory(connection, etfname, date):
    CollectionName = connection.ETF_db.ETFHoldings
    # Find ETFdbCategory for given ETF
    category_etf = CollectionName.find(
        {'FundHoldingsDate': {'$lte': datetime.datetime.strptime(date, '%Y%m%d')}, 'ETFTicker': etfname},
        {'_id': 0, 'ETFdbCategory': 1}).sort('-FundHoldingsDate').limit(1)
    # ETFdbCategory for given ETF
    category = str([item['ETFdbCategory'] for item in category_etf][0])
    # Find ETFs with same ETFdbCategory
    data = CollectionName.find({'ETFdbCategory': category},
                               {'FundHoldingsDate': 1, 'ETFTicker': 1, 'TotalAssetsUnderMgmt': 1, 'ETFName': 1,
                                '_id': 0}).sort('-FundHoldingsDate')
    combineddata = {}
    for item in data:
        if item['ETFTicker'] not in list(item.keys()):
            combineddata[item['ETFTicker']] = {'ETFName': item['ETFName'],
                                               'TotalAssetsUnderMgmt': item['TotalAssetsUnderMgmt']}

    return combineddata


def fetchETFsWithSimilarTotAsstUndMgmt(connection, date, etfname):
    CollectionName = connection.ETF_db.ETFHoldings
    # Find TotalAssetUnderMgmt for given ETF
    taum_etf = CollectionName.find(
        {'FundHoldingsDate': {'$lte':datetime.datetime.strptime(date, '%Y%m%d')}, 'ETFTicker': etfname},
        {'_id': 0, 'TotalAssetsUnderMgmt': 1}).sort('-FundHoldingsDate').limit(1)
    # TotalAssetUnderMgmt for given ETF
    taum = float([item['TotalAssetsUnderMgmt'] for item in taum_etf][0])
    # TotalAssetUnderMgmt for given ETF + 10%
    taumpos = taum * 1.1
    # TotalAssetUnderMgmt for given ETF - 10%
    taumneg = taum * 0.9
    # Find ETFs with TotalAssetUnderMgmt +/- 10% of given ETF's
    similar_taum_etfs = CollectionName.find(
        {'TotalAssetsUnderMgmt': {'$lte': taumpos, '$gte': taumneg}},
        {'FundHoldingsDate': 1, 'ETFTicker': 1, 'TotalAssetsUnderMgmt': 1, 'ETFName': 1,
         '_id': 0}).sort('-FundHoldingsDate')
    # List of Dicts
    combineddata = [{'ETFTicker': item['ETFTicker'],'ETFName': item['ETFName'], 'TotalAssetsUnderMgmt': item['TotalAssetsUnderMgmt']} for item in
                    similar_taum_etfs]
    return combineddata