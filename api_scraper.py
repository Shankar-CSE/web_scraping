"""
API Data Fetcher

This script demonstrates how to fetch data from public APIs.
APIs provide structured data (usually JSON) which is often easier
and more reliable than HTML scraping.

APIs used in this example:
- JSONPlaceholder (fake REST API for testing)
- GitHub API (public endpoints)
- OpenWeatherMap API concepts

Features covered:
- Making API requests
- Handling JSON responses
- API pagination
- Rate limiting
- Error handling
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime


class APIFetcher:
    """Base class for API data fetching with common utilities."""

    def __init__(self, base_url, rate_limit=1.0):
        """
        Initialize the API fetcher.

        Args:
            base_url: Base URL for the API
            rate_limit: Minimum seconds between requests
        """
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Python Web Scraping Tutorial/1.0'
        })

    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def get(self, endpoint, params=None):
        """
        Make a GET request to the API.

        Args:
            endpoint: API endpoint (will be appended to base_url)
            params: Optional query parameters

        Returns:
            JSON response data or None if request failed
        """
        self._wait_for_rate_limit()
        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None


def fetch_jsonplaceholder_data():
    """
    Fetch sample data from JSONPlaceholder API.
    This is a free fake API for testing and prototyping.
    """
    print("\n" + "="*50)
    print("JSONPlaceholder API Demo")
    print("="*50)

    api = APIFetcher("https://jsonplaceholder.typicode.com")

    # Fetch users
    print("\nFetching users...")
    users = api.get("users")
    if users:
        df_users = pd.DataFrame(users)
        print(f"Fetched {len(df_users)} users")
        print(df_users[['id', 'name', 'email', 'company']].head())

    # Fetch posts
    print("\nFetching posts...")
    posts = api.get("posts")
    if posts:
        df_posts = pd.DataFrame(posts)
        print(f"Fetched {len(df_posts)} posts")
        print(f"Posts per user:\n{df_posts['userId'].value_counts().head()}")

    # Fetch posts by specific user
    print("\nFetching posts by user 1...")
    user_posts = api.get("posts", params={'userId': 1})
    if user_posts:
        print(f"User 1 has {len(user_posts)} posts")

    return users, posts


def fetch_github_repos(username="octocat"):
    """
    Fetch public repositories from GitHub API.
    No authentication required for public data.

    Args:
        username: GitHub username to fetch repos for
    """
    print("\n" + "="*50)
    print(f"GitHub API Demo - Fetching repos for {username}")
    print("="*50)

    api = APIFetcher("https://api.github.com")

    # Fetch user info
    user_data = api.get(f"users/{username}")
    if user_data:
        print(f"\nUser: {user_data.get('name', username)}")
        print(f"Public repos: {user_data.get('public_repos', 0)}")
        print(f"Followers: {user_data.get('followers', 0)}")

    # Fetch repositories
    repos = api.get(f"users/{username}/repos", params={
        'sort': 'updated',
        'per_page': 10
    })

    if repos:
        print(f"\nLatest {len(repos)} repositories:")
        for repo in repos[:5]:
            stars = repo.get('stargazers_count', 0)
            language = repo.get('language', 'N/A')
            print(f"  - {repo['name']}: ⭐ {stars} | {language}")

        # Convert to DataFrame
        df_repos = pd.DataFrame(repos)
        return df_repos[['name', 'description', 'stargazers_count',
                         'forks_count', 'language', 'updated_at']]

    return None


def fetch_with_pagination(base_url, endpoint, max_pages=3, per_page=30):
    """
    Demonstrate pagination handling with APIs.

    Args:
        base_url: API base URL
        endpoint: API endpoint
        max_pages: Maximum number of pages to fetch
        per_page: Items per page

    Returns:
        Combined list of all items
    """
    print("\n" + "="*50)
    print("Pagination Demo")
    print("="*50)

    api = APIFetcher(base_url)
    all_items = []

    for page in range(1, max_pages + 1):
        data = api.get(endpoint, params={
            'page': page,
            'per_page': per_page
        })

        if not data:
            break

        all_items.extend(data)
        print(f"Page {page}: Fetched {len(data)} items (Total: {len(all_items)})")

        # Check if we've reached the end
        if len(data) < per_page:
            print("Reached last page")
            break

    return all_items


def save_api_data(data, filename, format='csv'):
    """
    Save fetched API data to file.

    Args:
        data: Data to save (list of dicts or DataFrame)
        filename: Output filename (without extension)
        format: 'csv' or 'json'
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data

    if format == 'csv':
        df.to_csv(f"{filename}.csv", index=False)
        print(f"Saved to {filename}.csv")
    elif format == 'json':
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')
        with open(f"{filename}.json", 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Saved to {filename}.json")


def main():
    """Run API fetching demonstrations."""
    print("API Data Fetching Examples")
    print("="*60)

    # Example 1: JSONPlaceholder
    users, posts = fetch_jsonplaceholder_data()
    if posts:
        save_api_data(posts, 'api_posts', 'csv')

    # Example 2: GitHub API
    repos = fetch_github_repos("octocat")
    if repos is not None:
        save_api_data(repos, 'github_repos', 'csv')

    print("\n" + "="*60)
    print("API fetching complete!")
    print("\nTips for working with APIs:")
    print("1. Always check the API documentation")
    print("2. Respect rate limits")
    print("3. Handle errors gracefully")
    print("4. Use authentication when required")
    print("5. Cache responses when appropriate")


if __name__ == "__main__":
    main()
