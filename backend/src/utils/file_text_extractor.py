from pdfminer.high_level import extract_text
from io import BytesIO

def extract_text_from_pdf(file_path: str) -> str:
    try:
        return extract_text(file_path)
    except Exception as e:
        print(f"Failed to extract text from PDF: {e}")
        return ""

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using pdfminer"""
    try:
        pdf_stream = BytesIO(pdf_bytes)
        return extract_text(pdf_stream)
    except Exception as e:
        print(f"Failed to extract text from PDF bytes: {e}")
        return ""

def extract_text_from_txt(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Failed to extract text from TXT: {e}")
        return ""

def extract_text_from_txt_bytes(txt_bytes: bytes) -> str:
    """Extract text from TXT bytes using UTF-8 decoding"""
    try:
        return txt_bytes.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return txt_bytes.decode('latin-1')
        except Exception as e:
            print(f"Failed to decode text bytes: {e}")
            return ""
    except Exception as e:
        print(f"Failed to extract text from TXT bytes: {e}")
        return ""