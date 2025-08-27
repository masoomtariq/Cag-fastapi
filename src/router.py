from fastapi import File, UploadFile, APIRouter
import os
from utils import extract_text

data_store = {}

file_router = APIRouter()

data_path = 'tmp/uploads'

os.makedirs(data_path, exist_ok=True)

@file_router.post('/add_file', status_code=201)
async def add_file(file: UploadFile = File(...)):

    file_path = os.path.join(data_path, file.filename)
    content = await file.read()
    

    return {'file_name': file.filename, 'file_path': file_path, "extracted_text": content}