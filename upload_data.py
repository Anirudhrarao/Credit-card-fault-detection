from pymongo.mongo_client import MongoClient
import pandas as pd 
import json

uri = "mongodb+srv://raorudhra16:3011@credit.u3fbkp8.mongodb.net/?retryWrites=true&w=majority" 

# create new client and connect to the server
client = MongoClient(uri)

# create database and collection name
DATABASE_NAME = 'Creditcardfault'
COLLECTION_NAME = 'CreditData'

# read data frame
df = pd.read_csv(r'dataset\UCI_Credit_Card.csv')

# convert data into json
json_records = list(json.loads(df.T.to_json()).values())

# dumping the json's record's in database
client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)


