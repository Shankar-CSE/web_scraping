"""
News Scraper - Hacker News

This script demonstrates how to scrape news articles from Hacker News.
Hacker News is a tech news aggregator with a simple HTML structure,
making it perfect for scraping practice.

Features covered:
- Scraping news headlines and metadata
- Extracting scores and comment counts
- Command-line interface
- JSON and CSV export options
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import argparse
from datetime import datetime


def scrape_hacker_news(num_pages=1):
    """
    Scrape stories from Hacker News.

    Args:
        num_pages: Number of pages to scrape (30 stories per page)

    Returns:
        List of dictionaries containing story data
    """
    base_url = "https://news.ycombinator.com"
    stories = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}/news?p={page}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all story rows
        story_rows = soup.find_all('tr', class_='athing')

        for story in story_rows:
            story_id = story.get('id')

            # Get title and link
            title_cell = story.find('span', class_='titleline')
            if not title_cell:
                continue

            title_link = title_cell.find('a')
            title = title_link.text if title_link else "No title"
            link = title_link.get('href', '') if title_link else ""

            # Get site domain if available
            site_span = title_cell.find('span', class_='sitestr')
            site = site_span.text if site_span else ""

            # Get metadata from the next row
            meta_row = story.find_next_sibling('tr')

            score = 0
            author = ""
            comments = 0
            time_posted = ""

            if meta_row:
                subtext = meta_row.find('td', class_='subtext')
                if subtext:
                    # Extract score
                    score_span = subtext.find('span', class_='score')
                    if score_span:
                        score_text = score_span.text
                        score = int(score_text.split()[0]) if score_text else 0

                    # Extract author
                    author_link = subtext.find('a', class_='hnuser')
                    author = author_link.text if author_link else ""

                    # Extract time
                    age_span = subtext.find('span', class_='age')
                    time_posted = age_span.text if age_span else ""

                    # Extract comments count
                    links = subtext.find_all('a')
                    for a in links:
                        if 'comment' in a.text.lower():
                            comment_text = a.text.split()[0]
                            try:
                                comments = int(comment_text)
                            except ValueError:
                                comments = 0

            stories.append({
                'id': story_id,
                'title': title,
                'url': link,
                'site': site,
                'score': score,
                'author': author,
                'comments': comments,
                'time_posted': time_posted,
                'scraped_at': datetime.now().isoformat()
            })

        print(f"Scraped page {page} - Total stories: {len(stories)}")

    return stories


def save_to_csv(data, filename='hacker_news.csv'):
    """Save scraped data to CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def save_to_json(data, filename='hacker_news.json'):
    """Save scraped data to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {filename}")


def display_summary(data):
    """Display summary statistics of scraped data."""
    df = pd.DataFrame(data)

    print("\n" + "="*50)
    print("SCRAPING SUMMARY")
    print("="*50)
    print(f"Total stories scraped: {len(df)}")
    print(f"\nTop 5 stories by score:")

    top_stories = df.nlargest(5, 'score')[['title', 'score', 'comments']]
    for _, row in top_stories.iterrows():
        print(f"  - {row['title'][:50]}... (Score: {row['score']}, Comments: {row['comments']})")

    print(f"\nAverage score: {df['score'].mean():.1f}")
    print(f"Average comments: {df['comments'].mean():.1f}")
    print(f"Most active author: {df['author'].value_counts().index[0] if len(df) > 0 else 'N/A'}")


def main():
    """Main function with CLI interface."""
    parser = argparse.ArgumentParser(
        description='Scrape stories from Hacker News',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python news_scraper.py                    # Scrape 1 page, save as CSV
  python news_scraper.py -p 3               # Scrape 3 pages
  python news_scraper.py -p 2 -o json       # Scrape 2 pages, save as JSON
  python news_scraper.py -p 5 -f hn_data    # Scrape 5 pages, custom filename
        """
    )

    parser.add_argument('-p', '--pages', type=int, default=1,
                        help='Number of pages to scrape (default: 1)')
    parser.add_argument('-o', '--output', choices=['csv', 'json', 'both'],
                        default='csv', help='Output format (default: csv)')
    parser.add_argument('-f', '--filename', type=str, default='hacker_news',
                        help='Output filename without extension (default: hacker_news)')

    args = parser.parse_args()

    print(f"Scraping {args.pages} page(s) from Hacker News...")
    stories = scrape_hacker_news(args.pages)

    if not stories:
        print("No stories scraped. Please check your internet connection.")
        return

    # Save based on output format
    if args.output in ['csv', 'both']:
        save_to_csv(stories, f"{args.filename}.csv")
    if args.output in ['json', 'both']:
        save_to_json(stories, f"{args.filename}.json")

    # Display summary
    display_summary(stories)


if __name__ == "__main__":
    main()
