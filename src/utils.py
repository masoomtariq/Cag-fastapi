import os
from pypdf import PdfReader

def extract_text(file_path):
    text = ''

    with open(file_path, 'rb') as f:
        reader = PdfReader(f)

    for i in reader:
        text += i

    return text