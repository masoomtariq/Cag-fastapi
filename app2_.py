from tempfile import TemporaryDirectory, NamedTemporaryFile, TemporaryFile
import os
from utils.file_processing import extract_text


with open('/workspaces/Cag/tmp/uploads/1_ASSIST Manual.pdf', 'rb') as file:
    with NamedTemporaryFile(dir='/workspaces/Cag/temp',
                            prefix='1_ASSIST Manual_', suffix='.pdf', delete=False) as tempfile:
        tempfile.write(file.read())

        text = extract_text(tempfile.read())
        print(tempfile.name)


print(text[:100])