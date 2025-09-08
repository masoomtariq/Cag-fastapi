
from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

now = datetime.now(ZoneInfo("Asia/Karachi"))

noww = now.isoformat(sep="\u002D", timespec='minutes') #"\u002D" is the unicode character of '-'

d = noww.split('-')

t = '--T->'.join(d)

print(t)
class FILE_INFO(BaseModel):
    title: str
    file_type: str
    uploaded_at: Annotated[datetime, Field(default=123)]
    size: int