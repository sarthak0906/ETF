from pymongo import MongoClient
# client = MongoClient('host', port_number)
client = MongoClient('localhost', 27017)
db = client.ETF_db
collection = db['ETFHoldings']
cursor = collection.find({})

for document in list(cursor):
	print(document)



'''
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient("localhost", 27017, maxPoolSize=50)
    db = client.localhost
    collection = db['chain']
    cursor = collection.find({})
    for document in cursor:
          print(document)
'''