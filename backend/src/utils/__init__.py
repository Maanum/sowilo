# Utils package for shared functionality

# Web scraping utilities
from .web_scraping import (
    fallback_html_fetcher,
    extract_text_from_html,
    fetch_and_extract_text,
    is_javascript_placeholder,
    fetch_with_playwright,
)

# File text extraction utilities
from .file_text_extractor import (
    extract_text_from_pdf,
    extract_text_from_pdf_bytes,
    extract_text_from_txt,
    extract_text_from_txt_bytes,
)

__all__ = [
    # Web scraping
    "fallback_html_fetcher",
    "extract_text_from_html", 
    "fetch_and_extract_text",
    "is_javascript_placeholder",
    "fetch_with_playwright",
    # File extraction
    "extract_text_from_pdf",
    "extract_text_from_pdf_bytes",
    "extract_text_from_txt",
    "extract_text_from_txt_bytes",
] 