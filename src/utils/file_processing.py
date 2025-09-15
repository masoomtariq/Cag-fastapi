from pypdf import PdfReader
from tempfile import NamedTemporaryFile
from db import file_exists
from fastapi import HTTPException

files_path = 'tmp/uploads'

def extract_text(file_path):
 
    full_text = []
    text = ''
    try:
        reader = PdfReader(file_path)
        for i in reader.pages:
            text = i.extract_text()
            if text:
                full_text.append(text)
        text = '\n'.join(full_text)
        return text + '\n\n'
    except FileNotFoundError:
        print(f"The file is not found at the path '{file_path}'")
        return ''
    
def load_and_extract(id, file_object):

    file_name, file_type = file_object.filename.split('.')
    if file_exists(file_name):
        raise HTTPException(status_code=401, detail=f"The file with name '{file_name}' already exists. Please rename the file and try again.")
    with NamedTemporaryFile(dir=files_path,
                                prefix=f'{id}_{file_name}_',
                                suffix=file_type, delete= True) as temp_file:
            temp_file.write(file_object.file.read())
            
            text = extract_text(temp_file.name)
            return text