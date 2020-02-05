import mongoengine


class Holdings(mongoengine.EmbeddedDocument):
    TickerName = mongoengine.StringField(unique=True)
    TickerSymbol = mongoengine.StringField(unique=True)
    TickerWeight = mongoengine.FloatField(unique=True)
