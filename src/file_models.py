from pydantic import BaseModel, Field
from typing import Annotated, List
from utils.helpers import datetime_func
from fastapi import UploadFile

class FILE_INFO(BaseModel):
    file_name: str
    file_title: str
    file_type: str
    file_content: str
    uploaded_at: Annotated[str, Field(default_factory=datetime_func)]
    size_mb: int | float

class FILES(BaseModel):
    id : int
    files: List[FILE_INFO]
    combined_content: str