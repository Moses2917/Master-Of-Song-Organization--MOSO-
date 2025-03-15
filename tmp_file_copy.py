import os
from os.path import join

doc_dir:str = "/Users/movsesmovsesyan/Documents/test_doc.docx"

def tmp_file_copy(doc_dir):
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp_dir:
        filename = doc_dir.split('/')[-1] # gets the filename
        tmp_file = os.path.join(filename, tempfile.tempdir)
        temp_file_path = shutil.copy(doc_dir, tmp_file)
        # Perform rest of ops in the 'with' statement

# tmp_file_copy(doc_dir)

import concurrent
from docx import Document

def tmp_file_copy(doc_dir):
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp_dir:
        filename = doc_dir.split('/')[-1] # gets the filename
        tmp_file = join(filename, tempfile.tempdir)
        temp_file_path: str = shutil.copy(doc_dir, tmp_file)
        # Perform rest of ops in the 'with' statement
        return Document(temp_file_path)

def async_call():
    import docx
    doc = tmp_file_copy(doc_dir) #Document(filePth)  # load doc file
    docParagraphs = doc.paragraphs
    print(docParagraphs)

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as futures:
    futures.submit(async_call).result()
    