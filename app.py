from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId
import time

from tempfile import TemporaryDirectory, NamedTemporaryFile

with TemporaryDirectory(prefix='tmp_', dir='/workspaces/Cag', delete=False) as tempdir:
    with NamedTemporaryFile(dir=tempdir, suffix='.txt', prefix='myfile', mode='r+t', delete=False) as file:

        file.write('THis is the smaple file')
        name = file.name

        with open(name, 'r') as f:
            text = file.read()
            print(text)

# load_dotenv()
# database_url = os.getenv("MONGO_URL")

# with MongoClient(database_url) as client:
#     cag = client['cag_app']
#     coll = cag['docs_data']
    

# time.sleep(0.2)
# client is closed automatically here