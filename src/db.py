from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import HTTPException
import os

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
        database.drop_collection('docs_data')

def file_exists(filename: str):

    collection = get_collection()
    file_names = collection.distinct('files.file_name')

    return filename in file_names