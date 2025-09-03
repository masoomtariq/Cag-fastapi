from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("MONGO_URL")

client = MongoClient(database_url)

client. 