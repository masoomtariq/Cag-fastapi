from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

connection_url = os.getenv('MONGO_URL')
# Create client once
client = MongoClient(connection_url)

# Select database & collection
db = client["cag_app"]
documents = db["documents"]