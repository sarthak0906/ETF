import sys  # Remove in production - KTZ

sys.path.append("..")  # Remove in production - KTZ
from pymongo import MongoClient


class MongoConnector():
    def connect_to_db(self, host, port):
        client = MongoClient(host, port)
        return client
    def disconnect_from_db(self, client):
        client.close()