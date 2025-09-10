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

def verify_id(id: int):
    with MongoClient(connection_url) as client:
        database = client['cag_app']
        collection = database['docs_data']
        collection.fin
        print(collection.list_indexes())

verify_id(2)