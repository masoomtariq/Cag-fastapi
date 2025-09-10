from schema import FILE_INFO
from fastapi import UploadFile

def create_file_info(file_object: UploadFile):
    title, filetype = file_object.filename.split(',')

    file_object.file.seek(0, 2)   # Move to end of file
    size_in_bytes = file_object.file.tell()  # Position = total size in bytes
    file_object.file.seek(0)      # Reset pointer back to start

    size_in_mb = round(size_in_bytes/(1024**2), 2)

    return FILE_INFO(title= title.strip(), file_type=filetype.strip(), size_mb= size_in_mb)