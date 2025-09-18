from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import HTTPException
import os

load_dotenv()
connection_url = os.getenv('MONGO_URL')

# One global MongoClient instance (thread-safe and reusable)
client = MongoClient(connection_url)
database = client["cag_app"]

def get_collection():
    """
    Get a reference to the 'docs_data' collection in 'cag_app' database.

    Returns:
        Collection: MongoDB collection object for 'docs_data'.
    """
    # Use context manager to ensure connection closes properly
    return database['docs_data']


def verify_id(id: int):
    """
    Verify if a document with the given ID exists in the collection.

    Args:
        id (int): Unique identifier of the document.

    Raises:
        HTTPException: If no document with the given ID exists.
    """
    collection = get_collection()
    if not collection.find_one({"id": id}):
        raise HTTPException(
            status_code=404,
            detail=f"The given id '{id}' does not exist."
        )


def delete_collection():
    """
    Drop the entire 'docs_data' collection from the database.
    Use with caution: This will remove all documents permanently.
    """
    with MongoClient(connection_url) as client:
        database = client['cag_app']
        database.drop_collection('docs_data')


def check_file_exists(filename: str):
    """
    Check if a file with the given name already exists in the collection.

    Args:
        filename (str): File name with extension (e.g., "document.pdf").

    Raises:
        HTTPException: If file already exists in the database.
    """
    collection = get_collection()
    
    # check if the filename is exists in the database.
    if collection.find_one({'files.file_name': filename}):
        raise HTTPException(
            status_code=409,
            detail=(
                f"The file with name '{filename}' already exists. "
                "Please rename the file and try again."
            )
        )
