import os
from io import BytesIO
from pathlib import Path
from typing import List, Optional

from core.config import settings
from docx import Document
from PyPDF2 import PdfReader


def validate_file_type(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in settings.ALLOWED_FILE_TYPES


def validate_file_size(file_size: int) -> bool:
    return file_size <= settings.MAX_FILE_SIZE


def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file_content))
        text = ""
        for page in reader.pages:
            txt = page.extract_text()
            if txt:
                text += txt + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")


def extract_text_from_docx(file_content: bytes) -> str:
    try:
        doc = Document(BytesIO(file_content))
        text = "\n".join(p.text for p in doc.paragraphs)
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {e}")


def extract_text_from_file(file_content: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_content)
    elif ext in {".docx", ".doc"}:
        return extract_text_from_docx(file_content)
    elif ext == ".txt":
        try:
            return file_content.decode("utf-8")
        except Exception as e:
            raise ValueError(f"Error decoding TXT file: {e}")
    else:
        raise ValueError(f"Unsupported file type {ext}")


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def cleanup_file(file_path: str):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)
