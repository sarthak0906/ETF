import datetime
import mongoengine
from holdings_mongo import Holdings


class ETF(mongoengine.Document):
    title = mongoengine.StringField()
    inception_date = mongoengine.DateTimeField()
    FundHoldings_date = mongoengine.DateTimeField()
    TotalAssetsUnderMgmt = mongoengine.IntField()
    SharesOutstanding = mongoengine.IntField()
    ExpenseRatio = mongoengine.FloatField()
    IndexTracker = mongoengine.StringField()
    ETFdbCategory = mongoengine.StringField()
    Issuer = mongoengine.StringField()
    Structure = mongoengine.StringField()
    ETFhomepage = mongoengine.StringField()

    holdings = mongoengine.EmbeddedDocumentListField(Holdings)

    meta = {
        'db_alias': 'ETF_db',
        'Collection': 'ETFHoldings'
    }
