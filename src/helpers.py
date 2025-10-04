from fastapi import Request, HTTPException
from datetime import datetime
from zoneinfo import ZoneInfo

def verify_id(id: int):
    """
    Verify if a document with the given ID exists in the collection.

    Args:
        id (int): Unique identifier of the document.

    Raises:
        HTTPException: If no document with the given ID exists.
    """
    collection = Request.app.state.collection
    if not collection.find_one({"id": id}):
        raise HTTPException(
            status_code=404,
            detail=f"The given id '{id}' does not exist."
        )

def check_file_exists(filename: str):
    """
    Check if a file with the given name already exists in the collection.

    Args:
        filename (str): File name with extension (e.g., "document.pdf").

    Raises:
        HTTPException: If file already exists in the database.
    """
    collection = Request.app.state.collection
    
    # check if the filename is exists in the database.
    if collection.find_one({'files.file_name': filename}):
        raise HTTPException(
            status_code=409,
            detail=(
                f"The file with name '{filename}' already exists. "
                "Please rename the file and try again."
            )
        )


def datetime_func() -> str:
    """
    Generate a timestamp string in ISO 8601 format with Asia/Karachi timezone.
    The default 'T' separator is replaced with '--T->' for custom readability.

    Returns:
        str: Formatted datetime string (up to minutes).
    """
    # Define timezone (Pakistan Standard Time)
    pkt_zone = ZoneInfo("Asia/Karachi")

    # Get the current datetime with timezone info
    now = datetime.now(pkt_zone)

    # Format to ISO string up to minutes (e.g., 2025-09-18T14:23)
    iso_format = now.isoformat(timespec="minutes")

    # Replace default 'T' with custom separator for readability
    return iso_format.replace("T", "--T->")
