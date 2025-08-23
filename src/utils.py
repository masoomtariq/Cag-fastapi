import os
import pdfreader

def extract_text(file_path):
    with open(file_path, 'rb') as f:
        reader = pdfreader(f)
