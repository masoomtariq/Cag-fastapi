from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
from utils.others import datetime_func

class FILE_INFO(BaseModel):
    title: str
    file_type: str
    uploaded_at: Annotated[datetime, Field(default_factory=datetime_func())]
    size: int

class FILES(BaseModel):
    