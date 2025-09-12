from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Dict
from fastapi import HTTPException
import os, time

load_dotenv()

connection_url = os.getenv('MONGO_URL')
def get_collection():
    with MongoClient(connection_url) as client:
        database = client['cag_app']
        collection = database['docs_data']
        return collection

ids = get_collection().distinct('id')
def verify_id(id: int):
    if id not in ids:
        raise HTTPException(status_code=401, detail=f"The given id '{id}' not exists.")
    
def delete_collection():
    with MongoClient(connection_url) as client:
        database = client['cag_app']
        database.drop_collection('docs_app')

