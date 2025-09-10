from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Dict
from fastapi import HTTPException
import os, time

load_dotenv()

connection_url = os.getenv('MONGO_URL')

with MongoClient(connection_url) as client:
    database = client['cag_app']
    collection = database['docs_data']

def verify_id(id: int):
    ids = collection.distinct('id')
    if id not in ids:
        raise HTTPException(status_code=401, detail=f"The given id '{id}' not exists.")

def add_file(FIlES: Dict):
    inserted = collection.insert_one(FIlES)

def update_file_data(id: int, file_data: Dict):
    collection.find_one_and_update({'id': id}, update=)