
from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

now = datetime.now(ZoneInfo("Asia/Karachi"))

print(f'{now} --- {type(now.ctime())}')

class FILE_INFO(BaseModel):
    title: str
    file_type: str
    uploaded_at: Annotated[datetime, Field(default=123)]
    size: int