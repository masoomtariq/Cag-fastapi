from fastapi import File, UploadFile, APIRouter, HTTPException, Path, Query
from utils.file_processing import load_and_extract
from db import get_collection, verify_id
from file_models import FILES, create_file_info
import os

files_path = 'tmp/uploads'
os.makedirs(files_path, exist_ok=True)

counter = 0
router = APIRouter()

@router.post('/upload', status_code=201)
def add_file(file: UploadFile = File(...)):

    global counter
    current_id = counter + 1

    
    extracted_text = load_and_extract(id=current_id, file_object=file) #id for naming the file
    
    if extracted_text is None:
        raise HTTPException(status_code=401, detail="Fail to extract text from the file.")
    counter +=1

    file_info = create_file_info(file_object=file)

    files_info = FILES(id=counter, files=[file_info], combined_content= extracted_text)

    collection = get_collection()
    collection.insert_one(files_info.model_dump())

    return {'message': "File uploaded and text extracted succesfully",
            'ID': counter}


@router.put('/update/{id}')
def update_the_existing_file(id: int, file: UploadFile = File(...)):

    verify_id(id=id)
    
    try:
        extracted_text = load_and_extract(id=id, file_object=file)

        if extracted_text is None:
            raise HTTPException(status_code=401, detail="Fail to extract text from the file.")

        file_data = create_file_info(file_object=file)
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