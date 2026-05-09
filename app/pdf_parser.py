import fitz  # PyMuPDF
from pathlib import Path
import os

# PDF text extraction 
def extract_text_from_pdf(pdf_path):
    
    document = fitz.open(pdf_path)

    pages = []

    for page_number in range(len(document)):
        page = document.load_page(page_number)
        text = page.get_text()
        pages.append({
            "page": page_number + 1,
            "text": text
        })

    return pages

# Split the text into chunks with overlap of 100 characters and chunk size of 500 characters
def chunk_text(text, chunk_size=500, overlap=100):
    
    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# PDF processing for one or more PDF files
def process_pdf(pdf_paths):

    if isinstance(pdf_paths, str):
        pdf_paths = [pdf_paths]
    
    all_chunks = []

    for pdf_path in pdf_paths:
        filename = Path(pdf_path).stem

        print(filename)

        pages = extract_text_from_pdf(pdf_path)

        for page in pages:
            page_chunks = chunk_text(page["text"])

            for idx, chunk in enumerate(page_chunks):
                all_chunks.append({
                    "text": chunk,
                    "metadata": {
                        "source": filename,
                        "page": page["page"],
                        "chunk_id": idx
                    }
                })

    return all_chunks
