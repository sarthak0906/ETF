import datetime
import mongoengine
#from ETFAnalysis.datafiles_mongo.holdings_mongo import Holdings
from HoldingsMongo import Holdings
import logging
from pymongo import monitoring

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} started on server "
                  "{0.connection_id}".format(event))

    def succeeded(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} on server {0.connection_id} "
                  "succeeded in {0.duration_micros} "
                  "microseconds".format(event))

    def failed(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} on server {0.connection_id} "
                  "failed in {0.duration_micros} "
                  "microseconds".format(event))


monitoring.register(CommandLogger())


class ETF(mongoengine.Document):
    title = mongoengine.StringField()
    inception_date = mongoengine.DateTimeField()
    FundHoldings_date = mongoengine.DateTimeField()
    TotalAssetsUnderMgmt = mongoengine.FloatField()
    SharesOutstanding = mongoengine.FloatField()
    ExpenseRatio = mongoengine.FloatField()
    IndexTracker = mongoengine.StringField()
    ETFdbCategory = mongoengine.StringField()
    Issuer = mongoengine.StringField()
    Structure = mongoengine.StringField()
    ETFhomepage = mongoengine.StringField()
    
    # New Ticker Values Added
    AverageVolume = mongoengine.StringField()
    Leveraged = mongoengine.StringField()
    Inversed = mongoengine.StringField()
    CommissionFree = mongoengine.StringField()
    AnnualDividendRate = mongoengine.StringField()
    DividendDate = mongoengine.StringField()
    Dividend = mongoengine.StringField()
    AnnualDividendYield = mongoengine.StringField()
    PERatio = mongoengine.StringField()
    Beta = mongoengine.StringField()
    NumberOfHolding = mongoengine.FloatField()
    OverAllRating = mongoengine.StringField()
    LiquidityRating = mongoengine.StringField()
    ExpensesRating = mongoengine.StringField()
    ReturnsRating = mongoengine.StringField()
    VolatilityRating = mongoengine.StringField()
    DividendRating = mongoengine.StringField()
    ConcentrationRating = mongoengine.StringField()
    ESGScore = mongoengine.FloatField()


    holdings = mongoengine.EmbeddedDocumentListField(Holdings)

    meta = {
        'indexes': [
            {
                'fields': ['title', 'FundHoldings_date'],
                'unique': True
            }
        ],
        'db_alias': 'ETF_db',
        'collection': 'ETFHoldings'
    }

# ETF.create_index({ETF.title: 1, ETF.FundHoldings_date: -1},{unique: True})
