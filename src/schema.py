from pydantic import BaseModel, Field
from typing import Annotated, List
from datetime import datetime
from utils.others import datetime_func

class FILE_INFO(BaseModel):
    title: str
    file_type: str
    uploaded_at: Annotated[str, Field(default_factory=datetime_func)]
    size_mb: int

class FILES(BaseModel):
    id : int
    files: List[FILE_INFO]
    combined_content: str