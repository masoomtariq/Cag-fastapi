from tempfile import TemporaryDirectory, NamedTemporaryFile, TemporaryFile
import os

with open('/workspaces/Cag/tmp/uploads/1_ASSIST Manual.pdf', 'rb') as file:
    with NamedTemporaryFile()