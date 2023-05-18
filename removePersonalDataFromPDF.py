import os
import re
import pdfplumber
from docx import Document

directory_path = "summarization-resume-vacancy-matching/pdf_after_preprocessing/pdf"

def modify_text(original_text):
    phone_regex = re.compile(r"(\+)?([0-9]{1,3})?( )?(\([0-9]{1,3}\))?( )?[(\d+((\-\d+)+)]{10,15}")
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
    url_regex = re.compile(r'http://\S+|https://\S+')
    address_regex = re.compile(r'\d+ [\w\s]+, [\w\s]+, [\w\s]+')
    phone_regex = re.compile(r'\+?[0-9]{1,3}[-\s]?(\([0-9]{1,3}\)[-.\s]?|[0-9]{1,3}[-.\s]?){1,2}[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}')
    linkedin_regex = re.compile(r'linkedin\.com\/in\/[a-zA-Z0-9_-]+')

    # Remove personal information from the original text
    modified_text = phone_regex.sub('', original_text)
    modified_text = email_regex.sub('', modified_text)
    modified_text = url_regex.sub('', modified_text)
    modified_text = address_regex.sub('', modified_text)
    modified_text = phone_regex.sub('', modified_text)
    modified_text = linkedin_regex.sub('', modified_text)

    # Remove non-XML compatible characters
    modified_text = remove_non_xml_chars(modified_text)
    
    return modified_text

import string

def remove_non_xml_chars(text):
    xml_compatible_text = re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '', text)
    return xml_compatible_text


def remove_personal_data(directory_path):
    for nameIndex, filename in enumerate(os.listdir(directory_path)):
        file_path = os.path.join(directory_path, filename)
        print(file_path)
        if filename.endswith(".pdf"):
            pdf = pdfplumber.open(file_path)
            doc = Document()
            numPages = len(pdf.pages)

            for number, page in enumerate(pdf.pages):
                pageText = page.extract_text()
                modified_text = modify_text(pageText)
                doc.add_paragraph(modified_text)

            new_filename = f"{nameIndex+14}.docx"
            doc.save(os.path.join('results2', new_filename))

remove_personal_data(directory_path)
