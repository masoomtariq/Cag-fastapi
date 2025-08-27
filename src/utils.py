import os
from pypdf import PdfReader

def initialize_counter():
    with open("")

def extract_text(file_path):
    text = ''

    reader = PdfReader(file_path)

    for i in reader.pages:
        text += i.extract_text()

    return text