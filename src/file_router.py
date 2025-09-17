from fastapi import File, UploadFile, APIRouter, HTTPException
from file_handler import File_Handler
from db import get_collection, verify_id, check_file_exists
import os

files_path = 'tmp/uploads'
os.makedirs(files_path, exist_ok=True)

counter = 0
router = APIRouter()

@router.post('/upload', status_code=201)
def add_file(file: UploadFile = File(...)):

    global counter
    current_id = counter + 1
    check_file_exists(file.filename)

    file_instance = File_Handler(user_id= current_id, file_object= file) #id for naming the file
    file_instance.load_and_process()

    files_data = file_instance.create_files_model()

    collection = get_collection()
    collection.insert_one(files_data)
    counter +=1
    
    return {'message': "File uploaded and text extracted succesfully",
            'ID': counter}

@router.put('/update/{id}')
def update_the_existing_file(id: int, file: UploadFile = File(...)):

    verify_id(id=id)
    check_file_exists(file.filename)
    
    try:
        file_instance = File_Handler(user_id= id, file_object=file) #id for naming the fil
        file_instance.load_and_process()
        file_data = file_instance.create_file_model()
        
        extracted_text = file_instance.file_content
        collection = get_collection()
        
        file_content = collection.find_one({'id': id})['combined_content'] + extracted_text
        collection.update_one({'id': id}, update={"$push": {'files': file_data},
                                                  
                                                  "$set": {'combined_content': file_content}})

        return {'message': "File uploaded and text updated successfully at the existing id",
                'ID': id}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error accured during the file processing: {str(e)}")

@router.delete('/delete/{id}')
def delete_file(id: int):

    verify_id(id=id)
    collection = get_collection()
    collection.delete_one({'id': id})

    return {"message": "The file/files has been deleted", "ID": id}