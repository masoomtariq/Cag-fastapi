from fastapi import File, UploadFile, APIRouter
import os


file_router = APIRouter()

data_path = 'temp/uploads'


@file_router.get('/add_file', status_code=201)
def add_file(file: UploadFile = File(...)):
    pass