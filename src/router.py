from fastapi import File, UploadFile, APIRouter
import os


file_router = APIRouter()

data_path = 'temp/uploads'

os.makedirs(data_path, exist_ok=True)

@file_router.get('/add_file', status_code=201)
def add_file(file: UploadFile = File(...)):
    
    file_path = os.path.join(data_path, file.filename)

    with open(file_path, 'wb') as f:
        f.write(file.file.read())

    