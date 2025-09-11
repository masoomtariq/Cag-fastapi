from fastapi import File, UploadFile, APIRouter, HTTPException, Path, Query
from utils.file_processing import load_and_extract
from utils.schema_helper import create_file_info
from utils.db import add_file, verify_id, update_file_data, delete_file
from schema import FILES
import os

files_path = 'tmp/uploads'
os.makedirs(files_path, exist_ok=True)

the_router = APIRouter()

@the_router.post('/upload', status_code=201)
def add_file(file: UploadFile = File(...)):

    global counter
    current_id = counter + 1

    
    extracted_text = load_and_extract(id=current_id, file_object=file) #id for naming the file
    
    if extracted_text is None:
        raise HTTPException(status_code=401, detail="Fail to extract text from the file.")
    counter +=1

    file_info = create_file_info(file_object=file)

    files_info = FILES(id=counter, files=[file_info], combined_content= extracted_text)

    add_file(file=files_info.model_dump())
    return {'message': "File uploaded and text extracted succesfully",
            'ID': counter}


@the_router.put('/update/{id}')
def update_the_existing_file(id: int, file: UploadFile = File(...)):

    verify_id(id=id)
    
    try:
        extracted_text = load_and_extract(id=id, file_object=file)

        if extracted_text is None:
            raise HTTPException(status_code=401, detail="Fail to extract text from the file.")

        file_data = create_file_info(file_object=file)
        update_file_data(id=id, file_data=file_data, file_text=extracted_text)

        return {'message': "File uploaded and text updated successfully at the existing id",
                'ID': id}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error accured during the file processing: {str(e)}")

@the_router.delete('/delete/{id}')
def delete_file(id: int):

    verify_id(id=id)
    
    delete_file(id=id)

    return {"message": "The file/files has been deleted", "ID": id}