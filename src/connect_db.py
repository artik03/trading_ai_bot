import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()

# currently not used in this project - instead saved to csv files locally - check helper.py

# connecting to mongo db to store data - on db side using Atlas mongoDB since its free and very easy to connect
# https://www.analyticsvidhya.com/blog/2022/10/using-mongodb-with-pandas-numpy-and-pyarrow/

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@data1.rrzwe9y.mongodb.net/?retryWrites=true&w=majority&appName=data1"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    


# fetched data storing and retriieving
db_name="trading_bot_data"
collection_name="binance"
    
def insert_dataframe(dataframe):
    # Convert DataFrame to dictionary
    data_dict = dataframe.to_dict("records")
    # Insert data into MongoDB
    db = client[db_name]
    collection = db[collection_name]
    result = collection.insert_many(data_dict)
    print(f"Inserted {len(result.inserted_ids)} records into {collection_name}.")
    
def fetch_dataframe_from_mongo():
    db = client[db_name]
    collection = db[collection_name]
    data = list(collection.find())
    
    # Convert to DataFrame
    dataframe = pd.DataFrame(data)
    
    # remove id column
    if '_id' in dataframe.columns:
        dataframe.drop(columns=['_id'], inplace=True)
    
    return dataframe