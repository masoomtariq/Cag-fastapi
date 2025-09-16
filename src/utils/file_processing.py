from pypdf import PdfReader
from tempfile import NamedTemporaryFile
from db import file_exists
from fastapi import HTTPException
from docx import Document
import pandas as pd
from pptx import Presentation

files_path = 'tmp/uploads'

def extract_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text + '\n\n'

def extract_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        text = '\n'.join(full_text)
        return text + '\n\n'
    except Exception as e:
        print(f"An error occurred while processing the DOCX file: {e}")
        return ''

def extract_pdf(file_path):
 
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

def extract_excel(file_path: str, file_type: str):
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type in ['xls', 'xlsx', 'excel']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def extract_pptx(file_path):
    text = []
    prs = Presentation(file_path)
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                text.append(shape.text)
    return text

def load_and_extract_file(id, file_object):

    file_name, file_type = file_object.filename.split('.')
    if file_exists(file_name):
        raise HTTPException(status_code=401, detail=f"The file with name '{file_name}' already exists. Please rename the file and try again.")
    with NamedTemporaryFile(dir=files_path,
                                prefix=f'{id}_{file_name}_',
                                suffix=file_type, delete= True) as temp_file:
            temp_file.write(file_object.file.read())
            
            text = extract_pdf(temp_file.name)
            return text