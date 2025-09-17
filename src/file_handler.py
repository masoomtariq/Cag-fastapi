from fastapi import UploadFile, HTTPException
from utils.file_processing import EXTRACTORS
from tempfile import NamedTemporaryFile
from file_models import FILE_INFO, FILES

files_path = 'tmp/uploads'

class File_Handler:
    def __init__(self, file_object: UploadFile, user_id: int):

        self.file_object = file_object
        self.user_id = user_id
        self.file_name = file_object.filename
        self.file_title, self.file_type = self.file_name.rsplit('.', 1)

        file_object.file.seek(0, 2)   # Move to end of file
        size_in_bytes = file_object.file.tell()  # Position = total size in bytes
        file_object.file.seek(0)      # Reset pointer back to start

        self.size_mb = round(size_in_bytes/(1024**2), 2)

    def load_and_process(self):

        with NamedTemporaryFile(dir=files_path,
                                prefix=f'{self.user_id}_{self.file_name}_',
                                suffix=f'.{self.file_type}', delete= True) as temp_file:
            temp_file.write(self.file_object.file.read())
            extractor = EXTRACTORS.get(self.file_type, None)
            
            if extractor is None:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {self.file_type}")
            try:
                extracted_text = extractor(temp_file.name)
            except Exception as e:
                raise HTTPException(
                status_code=500,
                detail=f"Error extracting text from {self.file_type.upper()} file: {str(e)}"
            )
            if extracted_text is None:
                raise HTTPException(status_code=401, detail="Fail to extract text from the file.")
            self.file_content = extracted_text

    def create_file_model(self):
        self.file_data = FILE_INFO(file_name=self.file_name,
                                   file_title=self.file_title,
                                   file_type=self.file_type,
                                   file_content=self.file_content,
                                   size_mb=self.size_mb)
        
        return self.file_data.model_dump()
    def create_files_model(self):
        self.file_data = FILE_INFO(file_name=self.file_name,
                                   file_title=self.file_title,
                                   file_type=self.file_type,
                                   file_content=self.file_content,
                                   size_mb=self.size_mb)
        
        self.files_data = FILES(id=self.user_id,
                                files=[self.file_data],
                                combined_content=self.file_content)
        
        return self.files_data.model_dump()