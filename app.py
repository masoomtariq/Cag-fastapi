from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()

database_url = os.getenv("MONGO_URL")

client = MongoClient(database_url)

cag = client.get_database('cag_app')

docs = cag.get_collection(name="documents")

d=docs.find()
print(d)