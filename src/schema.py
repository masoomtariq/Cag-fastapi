from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
from utils.others import datetime_func

class FILE_INFO(BaseModel):
    title: str
    file_type: str
    uploaded_at: Annotated[datetime, Field(default_factory=datetime_func())]
    size: int

df = FILE_INFO(title="VS code", file_type='pdf', size=456789)

print(df)