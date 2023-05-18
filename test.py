import re
import PyPDF2
from docx import Document

def modify_text(original_text):
    print(original_text)
    phone_regex = re.compile(r"(\+)?([0-9]{1,3})?( )?(\([0-9]{1,3}\))?( )?[(\d+((\-\d+)+)]{10,15}")
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
    url_regex = re.compile(r'http://\S+|https://\S+')

    # Remove personal information from the original text
    modified_text = phone_regex.sub('', original_text)
    modified_text = email_regex.sub('', modified_text)
    modified_text = url_regex.sub('', modified_text)
    
    return modified_text

# Open the original PDF file
with open('cv.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfFileReader(file)
    
    # Create a new Word document
    doc = Document()
   
    # Iterate over each page in the original PDF
    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        
        # Extract the original text content from the page
        original_text = page.extract_text()
        
        # Modify the text content as needed
        modified_text = modify_text(original_text)

        # Add the modified text to the Word document
        doc.add_paragraph(modified_text)

    # Save the modified text to a DOCX file
    doc.save('modified.docx')