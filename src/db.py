from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import HTTPException
import os

load_dotenv()

connection_url = os.getenv('MONGO_URL')
def get_collection():

    """Return reference to 'docs_data' collection."""

    with MongoClient(connection_url) as client:
        database = client['cag_app']
        collection = database['docs_data']
        return collection

def verify_id(id: int):

    """Check if a document with given ID exists."""

    collection = get_collection()
    if not collection.find_one({"id": id}):
        raise HTTPException(status_code=401, detail=f"The given id '{id}' not exists.")
   
def delete_collection():

    """Drop entire 'docs_data' collection."""
    
    with MongoClient(connection_url) as client:
        database = client['cag_app']
        database.drop_collection('docs_data')

def check_file_exists(filename: str):

    collection = get_collection()
    titles = collection.distinct('files.file_name')
    extensions = collection.distinct('files.file_type')
    files = [i+'.'+j for i, j in zip(titles, extensions)]

    if filename in files:
        raise HTTPException(status_code=401,
                                detail=f"The file with name '{filename}' already exists. Please rename the file and try again.")