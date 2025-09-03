from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import time

load_dotenv()
database_url = os.getenv("MONGO_URL")

with MongoClient(database_url) as client:
    cag = client['cag_app']
    coll = cag['docs_data']
    coll.insert_one()

time.sleep(0.2)
# client is closed automatically here