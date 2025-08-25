import os
import pdfreader

def extract_text(file_path):
    text = ''
    with open(file_path, 'rb') as f:
        reader = pdfreader(f)

    for i in reader:
        text += i

    return text