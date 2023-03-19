import os
from docx import Document

# Set the directory path where your .docx files are located
directory_path = "summarization-resume-vacancy-matching/docx_after_preprocessing/docx"

# Set the new name you want to use for the files
new_name = "new_file_name"
for i, filename in enumerate(os.listdir(directory_path)):
    if filename.endswith(".docx"):
        # Open the file with docx module
        doc = Document(os.path.join(directory_path, filename))
        
        # Do any necessary modifications to the document here
        
        # Save the modified document with a new name that includes an index
        new_filename = f"{new_name}{i}.docx"
        doc.save(os.path.join('results', new_filename))