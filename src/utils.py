import os
from pypdf import PdfReader

def initialize_counter():
    with open("counter.txt", 'w') as counter:
        counter.write('0')

with open("counter.txt", 'r') as file:
    counter = file.read()

def save_counter(updated_counter):
    with open("counter.txt", 'w') as file:
        file.write(str(updated_counter))

def extract_text(file_path):
    text = ''

    reader = PdfReader(file_path)

    for i in reader.pages:
        text += i.extract_text()

    return text

counter = int(counter)

print(type(counter))