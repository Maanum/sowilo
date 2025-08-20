# Backend Utils Module

This module contains shared utility functions that can be reused across different parts of the application.

## Web Scraping Utilities (`web_scraping.py`)

The web scraping utilities provide robust HTML fetching and text extraction capabilities with automatic fallback to Playwright for JavaScript-heavy pages.

### Functions

#### `fallback_html_fetcher(url: str) -> str`
Fetches HTML content from a URL with intelligent fallback to Playwright for JavaScript-heavy pages.

**Features:**
- First attempts simple HTTP request with proper headers
- Detects JavaScript-only pages automatically
- Falls back to Playwright for JavaScript rendering
- Handles timeouts and errors gracefully

**Usage:**
```python
from backend.utils.web_scraping import fallback_html_fetcher

html = fallback_html_fetcher("https://example.com")
```

#### `extract_text_from_html(html: str) -> str`
Extracts clean text content from HTML, removing scripts, styles, and other non-content elements.

**Features:**
- Removes script and style elements
- Cleans up whitespace and formatting
- Preserves meaningful text content

**Usage:**
```python
from backend.utils.web_scraping import extract_text_from_html

text = extract_text_from_html(html_content)
```

#### `fetch_and_extract_text(url: str) -> str`
Combines HTML fetching and text extraction in one convenient function.

**Usage:**
```python
from backend.utils.web_scraping import fetch_and_extract_text

text = fetch_and_extract_text("https://example.com")
```

#### `is_javascript_placeholder(html: str) -> bool`
Detects if HTML content contains JavaScript placeholder text indicating the page requires JavaScript.

**Usage:**
```python
from backend.utils.web_scraping import is_javascript_placeholder

needs_js = is_javascript_placeholder(html_content)
```

### Use Cases

#### 1. Job Description Parsing
```python
from backend.utils.web_scraping import fetch_and_extract_text

def parse_job_posting(url: str):
    # Extract text from job posting
    content = fetch_and_extract_text(url)
    
    # Send to LLM for structured extraction
    # ... LLM processing ...
    
    return job_data
```

#### 2. Profile Generation
```python
from backend.utils.web_scraping import fetch_and_extract_text

def generate_profile_from_links(links: List[str]):
    extracted_contents = []
    
    for link in links:
        try:
            content = fetch_and_extract_text(link)
            extracted_contents.append({
                'url': link,
                'content': content
            })
        except Exception as e:
            print(f"Failed to process {link}: {e}")
    
    # Process extracted content with LLM
    # ... LLM analysis ...
    
    return profile_entries
```

#### 3. Content Analysis
```python
from backend.utils.web_scraping import fallback_html_fetcher, extract_text_from_html

def analyze_webpage_content(url: str):
    # Get raw HTML for analysis
    html = fallback_html_fetcher(url)
    
    # Extract clean text
    text = extract_text_from_html(html)
    
    # Perform analysis
    # ... analysis logic ...
    
    return analysis_results
```

### Dependencies

The web scraping utilities require:
- `requests` - For HTTP requests
- `beautifulsoup4` - For HTML parsing
- `playwright` - For JavaScript rendering

These are already included in `backend/requirements.txt`.

### Error Handling

All functions include proper error handling:
- Network timeouts
- Invalid URLs
- JavaScript rendering failures
- HTML parsing errors

### Performance Considerations

- Simple HTTP requests are attempted first (faster)
- Playwright is only used when necessary (slower but more robust)
- Timeouts are set to prevent hanging requests
- User-Agent headers are included to avoid blocking

### Example Script

See `example_usage.py` for complete examples of how to use these utilities in different scenarios.

## Adding New Utilities

When adding new utility functions:

1. Create a new file in the `utils/` directory
2. Add proper imports and error handling
3. Include docstrings and type hints
4. Add examples in `example_usage.py` if applicable
5. Update this README with documentation 