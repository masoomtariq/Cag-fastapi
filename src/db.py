from pymongo import MongoClient
from dotenv import load_dotenv
import os, time

load_dotenv()

connection_url = os.getenv('MONGO_URL')

with MongoClient(connection_url) as client:
    
    db = client["cag_app"]
    
    data = db["docs_data"]
    h = data.find_one({'age': 20})

    print(h['age'])
