from fastapi import File, UploadFile, APIRouter, HTTPException
import os
from utils import extract_text

counter = 0
data_store = {}

file_router = APIRouter()

data_path = 'tmp/uploads'

os.makedirs(data_path, exist_ok=True)

@file_router.post('/add_file', status_code=201)
def add_file(file: UploadFile = File(...)):

    global counter
    global data_store

    file_path = os.path.join(data_path, file.filename)
    content = file.file.read()
    try:
        with open(file_path, 'wb') as f:
            f.write(content)

        extracted_text = extract_text(file_path)
        if extracted_text is None:
            raise HTTPException(status_code=401, detail="Fail to extract text from the file.")
        counter +=1
        data_store[counter] = extracted_text
        return {'message': "File uploaded and text extracted succesfully",
                'ID': counter}
    except Exception as e:
        counter -= 1
        raise HTTPException(status_code=500,
                            detail=f"An error accured during the file processing: {str(e)}")
