import os
from pypdf import PdfReader

def extract_text(file_path):
    full_text = []

    try:
        reader = PdfReader(file_path)
        for i in reader.pages:
            text += i.extract_text()
            if text:
                full_text.append(text)
        '/n'.join(full_text)
        return full_text
    except FileNotFoundError:
        print(f"The file is not found at the path '{file_path}'")
        return ''