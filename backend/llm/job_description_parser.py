import requests
from backend.llm.gpt_client import gpt_chat_complete
from backend.schemas import OpportunityCreate
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

SYSTEM_PROMPT = """
You are a job parser. Given raw text from a job posting, extract structured information
that matches this schema:

{
  title: str
  company: str
  level: Optional[str]
  min_salary: Optional[int]
  max_salary: Optional[int]
}

Respond only with a JSON object matching this schema. Do not explain your answer.
If salary is not found, leave it null. If level is not clear, leave it null.
"""

JS_PLACEHOLDER_STRINGS = [
    "You need to enable JavaScript to run this app.",
    "Please enable JavaScript",
    "Loading...",
]

def is_javascript_placeholder(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return any(phrase in text for phrase in JS_PLACEHOLDER_STRINGS) or len(text.strip()) < 100

def fetch_with_playwright(url: str) -> str:
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        html = page.content()
        browser.close()
        return html

def fallback_html_fetcher(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, timeout=10, headers=headers)
        html = resp.text
        if not is_javascript_placeholder(html):
            return html
        print(f"Detected JavaScript-only page, falling back to Playwright for {url}")
    except Exception as e:
        print(f"requests.get() failed for {url}: {e}")

    # Fallback: render page with Playwright
    try:
        return fetch_with_playwright(url)
    except Exception as e:
        raise RuntimeError(f"Playwright failed to load {url}: {e}")


def parse_opportunity_from_link(link: str) -> OpportunityCreate:

    job_description_content = fallback_html_fetcher(link)

    soup = BeautifulSoup(job_description_content, 'html.parser')
    for tag in soup(["script", "style", "nav", "footer", "head"]):
        tag.decompose()

    soup_text = soup.get_text(separator="\n", strip=True)
    gpt_response = gpt_chat_complete(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": soup_text}
        ]
    )
    
    parsed_opportunity = {
        **gpt_response,                      # Everything parsed by GPT
        "status": "To Apply",           # Override status
        "posting_link": link            # Override link
    }

    return OpportunityCreate(**parsed_opportunity)
