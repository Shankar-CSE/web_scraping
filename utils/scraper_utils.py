"""
Scraper Utilities

Common utility functions and classes for web scraping projects.
Import these to avoid code duplication across your scrapers.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from functools import wraps
from typing import Optional, Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Common User-Agent strings for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]


def get_random_user_agent() -> str:
    """Return a random User-Agent string."""
    return random.choice(USER_AGENTS)


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator that retries a function on failure.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
            raise last_exception
        return wrapper
    return decorator


class BaseScraper:
    """Base class for web scrapers with common functionality."""

    def __init__(
        self,
        base_url: str,
        rate_limit: float = 1.0,
        timeout: int = 10,
        rotate_user_agent: bool = True
    ):
        """
        Initialize the scraper.

        Args:
            base_url: Base URL for the website
            rate_limit: Minimum seconds between requests
            timeout: Request timeout in seconds
            rotate_user_agent: Whether to rotate User-Agent headers
        """
        self.base_url = base_url.rstrip('/')
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.rotate_user_agent = rotate_user_agent
        self.last_request_time = 0

        self.session = requests.Session()
        self._update_headers()

    def _update_headers(self):
        """Update session headers with a new User-Agent."""
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        if self.rotate_user_agent:
            headers['User-Agent'] = get_random_user_agent()
        self.session.headers.update(headers)

    def _wait_for_rate_limit(self):
        """Ensure we respect the rate limit."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    @retry_on_failure(max_retries=3, delay=1.0)
    def fetch(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """
        Fetch a URL and return parsed BeautifulSoup object.

        Args:
            url: URL to fetch (can be relative to base_url)
            params: Optional query parameters

        Returns:
            BeautifulSoup object or None if request failed
        """
        self._wait_for_rate_limit()

        if self.rotate_user_agent:
            self._update_headers()

        # Handle relative URLs
        if not url.startswith('http'):
            url = f"{self.base_url}/{url.lstrip('/')}"

        logger.info(f"Fetching: {url}")

        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        return BeautifulSoup(response.text, 'html.parser')

    def fetch_json(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Fetch a URL and return JSON response.

        Args:
            url: URL to fetch
            params: Optional query parameters

        Returns:
            JSON data as dictionary or None
        """
        self._wait_for_rate_limit()

        if not url.startswith('http'):
            url = f"{self.base_url}/{url.lstrip('/')}"

        logger.info(f"Fetching JSON: {url}")

        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        return response.json()


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra whitespace.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned text
    """
    if not text:
        return ""
    return ' '.join(text.split())


def extract_numbers(text: str) -> List[float]:
    """
    Extract all numbers from a string.

    Args:
        text: Text containing numbers

    Returns:
        List of extracted numbers
    """
    import re
    pattern = r'[-+]?\d*\.?\d+'
    matches = re.findall(pattern, text)
    return [float(m) for m in matches]


def extract_price(text: str) -> Optional[float]:
    """
    Extract price from text (handles various currency formats).

    Args:
        text: Text containing price

    Returns:
        Price as float or None
    """
    import re
    # Remove currency symbols and extract number
    cleaned = re.sub(r'[£$€¥₹,]', '', text)
    numbers = extract_numbers(cleaned)
    return numbers[0] if numbers else None


def save_to_csv(data: List[Dict], filename: str, **kwargs):
    """
    Save list of dictionaries to CSV file.

    Args:
        data: List of dictionaries to save
        filename: Output filename
        **kwargs: Additional arguments for pandas to_csv
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, **kwargs)
    logger.info(f"Saved {len(data)} records to {filename}")


def save_to_json(data: Any, filename: str, **kwargs):
    """
    Save data to JSON file.

    Args:
        data: Data to save
        filename: Output filename
        **kwargs: Additional arguments for json.dump
    """
    import json

    default_kwargs = {'indent': 2, 'ensure_ascii': False}
    default_kwargs.update(kwargs)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, **default_kwargs)

    logger.info(f"Saved data to {filename}")


def validate_url(url: str) -> bool:
    """
    Check if a URL is valid and accessible.

    Args:
        url: URL to validate

    Returns:
        True if URL is valid and accessible
    """
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_domain(url: str) -> str:
    """
    Extract domain from URL.

    Args:
        url: Full URL

    Returns:
        Domain name
    """
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return parsed.netloc


# Example usage
if __name__ == "__main__":
    print("Scraper Utilities Module")
    print("="*40)
    print("\nAvailable utilities:")
    print("- BaseScraper: Base class for scrapers")
    print("- get_random_user_agent(): Get a random User-Agent")
    print("- retry_on_failure: Decorator for retrying failed requests")
    print("- clean_text(): Clean extracted text")
    print("- extract_numbers(): Extract numbers from text")
    print("- extract_price(): Extract price from text")
    print("- save_to_csv(): Save data to CSV")
    print("- save_to_json(): Save data to JSON")
    print("- validate_url(): Check if URL is accessible")
    print("\nImport with: from utils.scraper_utils import *")
