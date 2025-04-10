import os
import re
import docx
import pdfplumber
from tempfile import SpooledTemporaryFile
from typing import Union
from io import BytesIO

def extract_text_from_pdf(file):
    """Extract text from a PDF file-like object."""
    text = ""
    try:
        file.seek(0)  # Reset pointer
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text.strip()

def extract_text_from_docx(file):
    """Extract text from a DOCX file-like object."""
    text = ""
    try:
        file.seek(0)  # Reset pointer
        doc = docx.Document(BytesIO(file.read()))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text.strip()

def extract_text_from_txt(file):
    """Extract text from a TXT file-like object."""
    try:
        file.seek(0)  # Reset pointer
        return file.read().decode("utf-8").strip()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return ""

def clean_text(text):
    """Clean and standardize extracted text."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces/newlines
    text = re.sub(r'[^\w\s,.-]', '', text)  # Remove unwanted special characters
    return text.strip()

def extract_text(file, file_ext=None):
    """Determine file type and extract text accordingly."""
    if file_ext is None:
        # Try to get file extension from the file name
        if hasattr(file, 'filename'):
            file_ext = os.path.splitext(file.filename)[1].lower()
        else:
            file_ext = os.path.splitext(file.name)[1].lower()
    
    if file_ext == ".pdf":
        text = extract_text_from_pdf(file)
    elif file_ext == ".docx":
        text = extract_text_from_docx(file)
    elif file_ext == ".txt":
        text = extract_text_from_txt(file)
    else:
        print(f"Unsupported file format: {file_ext}")
        return ""
    
    return clean_text(text)

# Example usage
if __name__ == "__main__":
    sample_resume = "../tests/sample_resume_1.pdf"  # Change to actual file path
    sample_job_desc = "../tests/job_description_1.txt"  # Change to actual file path
    
    resume_text = extract_text(sample_resume)
    job_desc_text = extract_text(sample_job_desc)
    
    print("Resume Text:\n", resume_text[:500])  # Print first 500 characters
    print("\nJob Description Text:\n", job_desc_text[:500])