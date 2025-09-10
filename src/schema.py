from pydantic import BaseModel, Field
from typing import Annotated, List
from datetime import datetime
from utils.others import datetime_func

class FILE_INFO(BaseModel):
    title: str
    file_type: str
    uploaded_at: Annotated[datetime, Field(default_factory=datetime_func())]
    size_mb: int

class FILES(BaseModel):
    id : str
    files: List[FILE_INFO]
    combined_content: str

files = FILES(id = 1, files=[FILE_INFO(title="this", file_type='dhl', size_mb=123)], combined_content='dkhfkjd')

print(files)