from fastapi import File, UploadFile, APIRouter, HTTPException
from utils import extract_text
import os

counter = 0
data_store = {}

the_router = APIRouter()

data_path = 'tmp/uploads'

os.makedirs(data_path, exist_ok=True)

@the_router.post('/upload', status_code=201)
def add_file(file: UploadFile = File(...)):

    global counter

    file_path = os.path.join(data_path, f"{counter+1}_{file.filename}")
    content = file.file.read()
    
    with open(file_path, 'wb') as f:
        f.write(content)

    extracted_text = extract_text(file_path)
    if extracted_text is None:
        raise HTTPException(status_code=401, detail="Fail to extract text from the file.")
    counter +=1
    data_store[counter] = extracted_text
    return {'message': "File uploaded and text extracted succesfully",
            'ID': counter}
    


@the_router.put('/update/{id}')
def update_the_existing_file(id: int, file: UploadFile = File(...)):

    if id not in data_store:
        raise HTTPException(status_code=401, detail=f"The given id '{id}' not exists.")
    
    global counter

    file_path = os.path.join(data_path, f"{counter}_{file.filename}")
    content = file.file.read()
    try:
        with open(file_path, 'wb') as f:
            f.write(content)

        extracted_text = extract_text(file_path)
        if extracted_text is None:
            raise HTTPException(status_code=401, detail="Fail to extract text from the file.")
        data_store[counter] += extracted_text
        return {'message': "File uploaded and text updated successfully at the existing id",
                'ID': counter}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error accured during the file processing: {str(e)}")

@the_router.delete('/delete/{id}')
def delete_file(id: int):
    if id not in data_store:
        raise HTTPException(status_code=401, detail=f"The given id '{id}' not exists.")
    files = os.listdir(data_path)
    for file in files:
        if file.startswith(f'{str(id)}_'):
            path = f'{data_path}/{file}'
            os.remove(path)
    del data_store[id]

    return {"message": "The file/files has been deleted", "ID": id}

