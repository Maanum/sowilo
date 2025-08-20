import asyncio
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Common JavaScript placeholder strings that indicate a page needs JS to render
JS_PLACEHOLDER_STRINGS = [
    "You need to enable JavaScript to run this app.",
    "Please enable JavaScript",
    "Loading...",
    "JavaScript is required",
    "Enable JavaScript to continue",
]


def is_javascript_placeholder(html: str) -> bool:
    """
    Check if the HTML content contains JavaScript placeholder text
    indicating the page requires JavaScript to render properly.
    """
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return (
        any(phrase in text for phrase in JS_PLACEHOLDER_STRINGS)
        or len(text.strip()) < 100
    )


async def fetch_with_playwright(url: str) -> str:
    """
    Fetch HTML content using Playwright to handle JavaScript-rendered pages.
    """
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")
        html = await page.content()
        await browser.close()
        return html


def extract_github_content(html: str, url: str) -> str:
    """
    Extract meaningful content from GitHub repository pages.

    Args:
        html: Raw HTML content from GitHub
        url: The GitHub URL

    Returns:
        Structured content from the repository
    """
    soup = BeautifulSoup(html, "html.parser")
    content_parts = []

    # Extract repository name and description
    repo_name_elem = soup.find("strong", {"itemprop": "name"})
    if repo_name_elem:
        content_parts.append(f"Repository: {repo_name_elem.get_text().strip()}")

    description_elem = soup.find("div", {"class": "repository-description"})
    if description_elem:
        content_parts.append(f"Description: {description_elem.get_text().strip()}")

    # Extract README content
    readme_elem = soup.find("div", {"id": "readme"})
    if readme_elem:
        readme_content = readme_elem.get_text(separator="\n", strip=True)
        content_parts.append(f"README:\n{readme_content}")

    # Extract topics/tags
    topics = soup.find_all("a", {"class": "topic-tag"})
    if topics:
        topic_text = ", ".join([topic.get_text().strip() for topic in topics])
        content_parts.append(f"Topics: {topic_text}")

    # Extract language statistics
    lang_elem = soup.find("span", {"class": "language-color"})
    if lang_elem:
        lang_name = lang_elem.find_next_sibling()
        if lang_name:
            content_parts.append(f"Primary Language: {lang_name.get_text().strip()}")

    # Extract star count and other stats
    stats = soup.find_all("a", {"class": "social-count"})
    for stat in stats:
        stat_text = stat.get_text().strip()
        if stat_text:
            content_parts.append(f"Stats: {stat_text}")

    # If no specific content found, fall back to general text extraction
    if not content_parts:
        return extract_text_from_html(html)

    return "\n\n".join(content_parts)


async def fallback_html_fetcher(url: str) -> str:
    """
    Fetch HTML content from a URL with fallback to Playwright for JavaScript-heavy pages.

    Args:
        url: The URL to fetch HTML from

    Returns:
        The HTML content as a string

    Raises:
        RuntimeError: If both requests and Playwright fail to load the URL
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    # First try: simple HTTP request
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
        return await fetch_with_playwright(url)
    except Exception as e:
        raise RuntimeError(f"Playwright failed to load {url}: {e}")


def extract_text_from_html(html: str) -> str:
    """
    Extract clean text content from HTML, removing scripts, styles, and other non-content elements.

    Args:
        html: Raw HTML content

    Returns:
        Clean text content
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text and clean it up
    text = soup.get_text(separator="\n", strip=True)

    # Remove excessive whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


async def fetch_and_extract_text(url: str) -> str:
    """
    Fetch HTML from a URL and extract clean text content.
    Special handling for GitHub repositories.

    Args:
        url: The URL to fetch content from

    Returns:
        Clean text content from the webpage
    """
    html = await fallback_html_fetcher(url)

    # Special handling for GitHub repositories
    if "github.com" in url and "/" in url.split("github.com/")[-1]:
        print(f"Detected GitHub repository: {url}")
        return extract_github_content(html, url)

    return extract_text_from_html(html)


def fetch_and_extract_text_sync(url: str) -> str:
    """
    Synchronous wrapper for fetch_and_extract_text.
    """
    return asyncio.run(fetch_and_extract_text(url))
