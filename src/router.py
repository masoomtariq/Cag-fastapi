from fastapi import File, UploadFile, APIRouter
import os
from utils import extract_text

file_router = APIRouter()

data_path = 'temp/uploads'

os.makedirs(data_path, exist_ok=True)

@file_router.post('/add_file', status_code=201)
async def add_file(file: UploadFile = File(...)):
    
    file_path = os.path.join(data_path, file.filename)
    content = await file.read()
    with open(file_path, 'wb') as f:
        f.write(content)

    extracted = extract_text(file_path)

    return {'file_name': file.filename, 'file_path': file_path, "extracted_text": extracted}