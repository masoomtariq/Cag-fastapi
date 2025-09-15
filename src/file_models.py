from pydantic import BaseModel, Field
from typing import Annotated, List
from utils.helpers import datetime_func
from fastapi import UploadFile

class FILE_INFO(BaseModel):
    file_name: str
    file_type: str
    uploaded_at: Annotated[str, Field(default_factory=datetime_func)]
    size_mb: int | float

class FILES(BaseModel):
    id : int
    files: List[FILE_INFO]
    combined_content: str

def create_file_info(file_object: UploadFile) -> dict:
    title, filetype = file_object.filename.split('.')

    file_object.file.seek(0, 2)   # Move to end of file
    size_in_bytes = file_object.file.tell()  # Position = total size in bytes
    file_object.file.seek(0)      # Reset pointer back to start

    size_in_mb = round(size_in_bytes/(1024**2), 2)

    return FILE_INFO(file_name=title.strip(), file_type=filetype.strip(), size_mb= size_in_mb).model_dump()