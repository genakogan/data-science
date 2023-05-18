# Import required library.
import pdfplumber
from docx import Document





# Open the file and create a pdf object.
pdf = pdfplumber.open("cv.pdf")
doc = Document()
# Get the number of pages.
numPages = len(pdf.pages)

print("Number of Pages:", numPages)

# Iterate over each page and extract the text of each page.
for number, pageText in enumerate(pdf.pages):
    print("Page Number:", number)
    print(pageText.extract_text())
    
    doc.add_paragraph(pageText.extract_text())

    doc.save('modified.docx')