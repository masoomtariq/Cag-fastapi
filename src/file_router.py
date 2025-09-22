import os
from fastapi import File, UploadFile, APIRouter, HTTPException
from file_handler import File_Handler
from db import get_collection, verify_id, check_file_exists

# Directory where uploaded files are temporarily stored
files_path = "tmp/uploads"
os.makedirs(files_path, exist_ok=True)  # Ensure folder exists at startup

# Global counter to assign IDs (⚠️ Note: resets if server restarts)
counter = 0

# FastAPI router for file-related endpoints
router = APIRouter()


@router.post("/upload", status_code=201)
async def add_file(file: UploadFile = File(...)):
    """
    Upload a new file, extract its content, and save it to MongoDB.

    Args:
        file (UploadFile): File uploaded by the user.

    Returns:
        dict: Confirmation message with assigned ID.
    """
    global counter
    current_id = counter + 1

    # Prevent duplicate filenames in DB
    await check_file_exists(file.filename)

    # Process file (extract content + metadata)
    file_instance = File_Handler(user_id=current_id, file_object=file)
    await file_instance.load_and_process()

    # Build FILES model and save to DB
    files_data = file_instance.create_files_model()
    collection = get_collection()
    await collection.insert_one(files_data)

    counter += 1  # Update global counter

    return {"message": "File uploaded and text extracted successfully", "ID": counter}


@router.put("/update/{id}")
async def update_the_existing_file(id: int, file: UploadFile = File(...)):
    """
    Upload a new file and append it to an existing user ID.

    Args:
        id (int): Existing user/document ID.
        file (UploadFile): New file to be added.

    Returns:
        dict: Confirmation message with the updated ID.
    """
    # Ensure the document exists & filename is unique
    await verify_id(id=id)
    await check_file_exists(file.filename)

    try:
        # Process the new file
        file_instance = File_Handler(user_id=id, file_object=file)
        await file_instance.load_and_process()
        file_data = file_instance.create_file_model()
        extracted_text = file_instance.file_content

        collection = get_collection()

        # Append new file + update combined content
        # Fetch existing combined content
        doc = await collection.find_one({"id": id})
        file_content = doc["combined_content"] + extracted_text
        await collection.update_one(
            {"id": id},
            update={
                "$push": {"files": file_data},
                "$set": {"combined_content": file_content},
            },
        )

        return {
            "message": "File uploaded and text updated successfully at the existing ID",
            "ID": id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file processing: {str(e)}",
        )


@router.delete("/delete/{id}")
async def delete_file(id: int):
    """
    Delete all files associated with a given ID.

    Args:
        id (int): User/document ID.

    Returns:
        dict: Confirmation message with deleted ID.
    """
    await verify_id(id=id)
    collection = get_collection()
    await collection.delete_one({"id": id})

    return {"message": "The file/files has been deleted", "ID": id}