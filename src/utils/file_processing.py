from fastapi import UploadFile
from pypdf import PdfReader
from tempfile import NamedTemporaryFile
from db import file_exists
from fastapi import HTTPException
from docx import Document
import pandas as pd
from pptx import Presentation
import ebooklib
from bs4 import BeautifulSoup
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

files_path = 'tmp/uploads'

def extract_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text + '\n\n'

def extract_pdf(file_path):
 
    full_text = []
    text = ''
    try:
        reader = PdfReader(file_path)
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                full_text.append(text.strip())
            else:
                images = convert_from_path(file_path, first_page=index+1, last_page=index+1)
                if images:
                    ocr_text = pytesseract.image_to_string(images[0]).strip()
                    if ocr_text:
                        full_text.append(ocr_text)
        text = '\n'.join(full_text)
        return text + '\n\n'
    except FileNotFoundError:
        print(f"The file is not found at the path '{file_path}'")
        return ''

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

def extract_excel(file_path: str):

    file_type = file_path.rsplit('.')[-1].lower()
    if file_type == 'csv':
        df = pd.read_csv(file_path)
        return df.to_string() + '\n\n'
    elif file_type in ['xls', 'xlsx', 'excel']:
        df = pd.read_excel(file_path)
        return df.to_string() + '\n\n'
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def extract_pptx(file_path):

    text = []
    prs = Presentation(file_path)

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text.append(shape.text)
        text.append('\n')
    text.append('\n')
    return '\n'.join(text)

def extract_epub(file_path):

    text = []
    book = ebooklib.epub.read_epub(file_path)
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), "html.parser")
            text.append(soup.get_text())
    text.append('\n')
    return '\n'.join(text)

def extract_image(file_path):
    text = pytesseract.image_to_string(Image.open(file_path))
    return text

EXTRACTORS = {
    "pdf": extract_pdf,
    "txt": extract_txt,
    "docx": extract_docx,
    "pptx": extract_pptx,
    "epub": extract_epub,
    "xls": extract_excel,
    "xlsx": extract_excel,
    "csv": extract_excel,
    "jpg": extract_image,
    "jpeg": extract_image,
    "png": extract_image,
    "tif": extract_image,
    "bmp": extract_image,
    "gif": extract_image,
    "webp": extract_image
}

def load_and_extract_file(id: int, file_object: UploadFile):

    file_name, file_type = file_object.filename.rsplit('.', 1)
    file_type = file_type.lower()

    if file_exists(file_object.filename):
        raise HTTPException(status_code=401, detail=f"The file with name '{file_name}' already exists. Please rename the file and try again.")
    
    with NamedTemporaryFile(dir=files_path,
                                prefix=f'{id}_{file_name}_',
                                suffix=f'.{file_type}', delete= True) as temp_file:
            temp_file.write(file_object.file.read())
            extractor = EXTRACTORS.get(file_type, None)
            
            if extractor is None:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")
            try:
                return extractor(temp_file.name)
            except Exception as e:
                raise HTTPException(
                status_code=500,
                detail=f"Error extracting text from {file_type.upper()} file: {str(e)}"
            )