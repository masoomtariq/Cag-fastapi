from datetime import datetime
from zoneinfo import ZoneInfo

def datetime_func():
    pkt_zone = ZoneInfo("Asia/Karachi")

    now = datetime.now(ZoneInfo("Asia/Karachi"))

    iso_format = now.isoformat(timespec='minutes') #'sep' argument takes the unicode character i.e "\u002D" represents '-'

    splitted = iso_format.split('T')

    return '--T->'.join(splitted)