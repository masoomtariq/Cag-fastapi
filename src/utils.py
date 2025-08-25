import os
from pypdf import PdfReader


reader = PdfReader('/workspaces/Cag/temp/uploads/ASSIST Manual.pdf')

print(reader.pages)

    