from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Dict
import os, time

load_dotenv()

connection_url = os.getenv('MONGO_URL')

def add_file(FIlES: Dict):
    with MongoClient(connection_url) as client:
        database = client['cag_app']
        collection = database['docs_data']

        inserted = collection.insert_one(FIlES)

    time.sleep(0.2)