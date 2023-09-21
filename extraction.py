import PyPDF2
import csv

pdf_file_path = 'spaceM6.pdf'

with open(pdf_file_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_content = ''
   
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text_content += page.extract_text()

rows = text_content.split('\n')
csv_file_path = 'spaceM6.csv'


with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    for row in rows:
        csv_writer.writerow([row])

print("CSV file created successfully.")
