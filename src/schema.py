from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
from zoneinfo import ZoneInfo

pkt_zone = ZoneInfo("Asia/Karachi")

now = datetime.now(ZoneInfo("Asia/Karachi"))

noww = now.isoformat(timespec='minutes') #'sep' argument takes the unicode character i.e "\u002D" represents '-'

d = noww.split('T')

t = '--T->'.join(d)
print(t)

class FILE_INFO(BaseModel):
    title: str
    file_type: str
    uploaded_at: Annotated[datetime, Field(default_factory= datetime.now(pkt_zone))]
    size: int

df = FILE_INFO(title="VS code", file_type='pdf', size=456789)

# print(df)