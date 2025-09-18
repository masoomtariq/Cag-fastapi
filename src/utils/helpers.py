from datetime import datetime
from zoneinfo import ZoneInfo

def datetime_func() -> str:
    """
    Generate a timestamp string in ISO 8601 format with Asia/Karachi timezone.
    The default 'T' separator is replaced with '--T->' for custom readability.

    Returns:
        str: Formatted datetime string (up to minutes).
    """
    # Define timezone (Pakistan Standard Time)
    pkt_zone = ZoneInfo("Asia/Karachi")

    # Get the current datetime with timezone info
    now = datetime.now(pkt_zone)

    # Format to ISO string up to minutes (e.g., 2025-09-18T14:23)
    iso_format = now.isoformat(timespec="minutes")

    # Replace default 'T' with custom separator for readability
    return iso_format.replace("T", "--T->")
