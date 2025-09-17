from fastapi import UploadFile
from utils.file_processing import EXTRACTORS, load_and_extract_file

class File_Handler:
    def __init__(self, file_object: UploadFile, user_id: int):
        self.user_id = user_id
        self.file_name = file_object.filename
        self.file_title, self.file_type = self.file_name.rsplit(',', 1)

        file_object.file.seek(0, 2)   # Move to end of file
        size_in_bytes = file_object.file.tell()  # Position = total size in bytes
        file_object.file.seek(0)      # Reset pointer back to start

        self.size_mb = round(size_in_bytes/(1024**2), 2)

    def process():
        pass
    
            