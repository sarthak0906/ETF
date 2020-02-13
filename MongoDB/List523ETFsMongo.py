import datetime
import mongoengine
from MongoDB.ETFListCollection import ETFListData
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

class ETFListDocument(mongoengine.Document):
    Download_date = mongoengine.DateField()
    etflist = mongoengine.EmbeddedDocumentListField(ETFListData)

    meta = {
        'indexes': [
            {
                'fields': ['Download_date'],
                'unique': True
            }
        ],
        'db_alias': 'ETF_db',
        'collection': 'ETF523List'
    }