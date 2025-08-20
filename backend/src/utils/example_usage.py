"""
Example usage of the web scraping utilities from utils.web_scraping

This script demonstrates how to use the fallback_html_fetcher and related functions
for different web scraping scenarios.
"""

from utils.web_scraping import (
    fallback_html_fetcher,
    extract_text_from_html,
    fetch_and_extract_text,
    is_javascript_placeholder
)

def example_basic_fetching():
    """Example of basic HTML fetching"""
    url = "https://example.com"
    
    try:
        # Fetch raw HTML
        html = fallback_html_fetcher(url)
        print(f"Successfully fetched HTML from {url}")
        print(f"HTML length: {len(html)} characters")
        
        # Extract clean text
        text = extract_text_from_html(html)
        print(f"Extracted text length: {len(text)} characters")
        print(f"First 200 characters: {text[:200]}...")
        
    except Exception as e:
        print(f"Error fetching {url}: {e}")

def example_text_extraction():
    """Example of fetching and extracting text in one step"""
    url = "https://example.com"
    
    try:
        # Fetch and extract text in one step
        text = fetch_and_extract_text(url)
        print(f"Successfully extracted text from {url}")
        print(f"Text length: {len(text)} characters")
        
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")

def example_javascript_detection():
    """Example of detecting JavaScript-heavy pages"""
    # This would be useful for determining if a page needs Playwright
    html_content = """
    <html>
        <body>
            <div>You need to enable JavaScript to run this app.</div>
        </body>
    </html>
    """
    
    is_js_required = is_javascript_placeholder(html_content)
    print(f"JavaScript required: {is_js_required}")

def example_profile_generation_workflow():
    """Example workflow for profile generation using web scraping"""
    # Simulate profile generation with links
    profile_links = [
        "https://linkedin.com/in/example",
        "https://github.com/example",
        "https://portfolio.example.com"
    ]
    
    extracted_data = []
    
    for link in profile_links:
        try:
            print(f"Processing link: {link}")
            
            # Extract text content
            content = fetch_and_extract_text(link)
            
            # Store extracted data
            extracted_data.append({
                'url': link,
                'content': content,
                'content_length': len(content)
            })
            
            print(f"Successfully extracted {len(content)} characters from {link}")
            
        except Exception as e:
            print(f"Failed to process {link}: {e}")
    
    print(f"Successfully processed {len(extracted_data)} out of {len(profile_links)} links")
    
    # In a real implementation, you would:
    # 1. Send the extracted content to an LLM for analysis
    # 2. Parse the LLM response to extract structured profile data
    # 3. Create profile entries based on the analysis
    
    return extracted_data

if __name__ == "__main__":
    print("=== Web Scraping Utilities Example ===\n")
    
    print("1. Basic HTML fetching:")
    example_basic_fetching()
    print()
    
    print("2. Text extraction:")
    example_text_extraction()
    print()
    
    print("3. JavaScript detection:")
    example_javascript_detection()
    print()
    
    print("4. Profile generation workflow:")
    example_profile_generation_workflow()
    print()
    
    print("=== Example completed ===") 