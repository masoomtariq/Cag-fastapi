from fastapi import UploadFile

class File_Handler:
    def __init__(self, file_object: UploadFile, user_id: int):
        self.user_id = user_id
        self.file_name = file_object.filename
        self.file_title, self.file_type = self.file_name.rsplit(',', 1)
        