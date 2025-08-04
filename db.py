from pymongo import MongoClient
import os

from dotenv import load_dotenv
load_dotenv()



client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)
client.server_info()
db = client.get_database(os.getenv("MONGO_DB_NAME"))
collection = db.get_collection(os.getenv("MONGO_COLLECTION_NAME"))  
collection2 = db.get_collection(os.getenv("MONGO_COLLECTION2_NAME"))  