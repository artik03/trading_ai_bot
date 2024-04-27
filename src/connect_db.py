from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()

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