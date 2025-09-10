from datetime import datetime
from zoneinfo import ZoneInfo
from schema import FILE_INFO, FILES
from fastapi import UploadFile
import os
def datetime_func():
    pkt_zone = ZoneInfo("Asia/Karachi")

    now = datetime.now(ZoneInfo("Asia/Karachi"))

    iso_format = now.isoformat(timespec='minutes') #'sep' argument takes the unicode character i.e "\u002D" represents '-'

    splitted = iso_format.split('T')

    return '--T->'.join(splitted)

def create_model(file_object: UploadFile):
    title, filetype = file_object.filename.split(',')
    size= os.path.getsize(file)
    FILE_INFO(title= title.strip(), file_type=filetype.strip(), s)