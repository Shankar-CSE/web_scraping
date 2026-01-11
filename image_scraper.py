"""
Image Scraper

This script demonstrates how to download images from websites.
It includes techniques for finding image URLs and downloading them.

Features covered:
- Finding image elements in HTML
- Handling relative URLs
- Downloading and saving images
- Creating organized output directories
- Progress tracking

Note: Always respect copyright and website terms of service
when downloading images.
"""

from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin, urlparse
import time
import hashlib


class ImageScraper:
    """A class to scrape and download images from websites."""

    def __init__(self, output_dir='downloaded_images'):
        """
        Initialize the image scraper.

        Args:
            output_dir: Directory to save downloaded images
        """
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.downloaded = set()

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def get_image_urls(self, url, min_size=None):
        """
        Extract all image URLs from a webpage.

        Args:
            url: The webpage URL to scrape
            min_size: Minimum image size (width, height) tuple or None

        Returns:
            List of absolute image URLs
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        image_urls = []

        # Find all <img> tags
        for img in soup.find_all('img'):
            # Try different attributes for image source
            img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')

            if img_url:
                # Convert relative URL to absolute
                absolute_url = urljoin(url, img_url)

                # Filter by size if specified
                if min_size:
                    width = img.get('width', '0')
                    height = img.get('height', '0')
                    try:
                        w = int(str(width).replace('px', ''))
                        h = int(str(height).replace('px', ''))
                        if w < min_size[0] or h < min_size[1]:
                            continue
                    except ValueError:
                        pass

                image_urls.append(absolute_url)

        # Also check for background images in style attributes
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            if 'background-image' in style:
                # Extract URL from background-image: url('...')
                import re
                match = re.search(r'url\([\'"]?([^\'"]+)[\'"]?\)', style)
                if match:
                    img_url = urljoin(url, match.group(1))
                    image_urls.append(img_url)

        return list(set(image_urls))  # Remove duplicates

    def download_image(self, url, filename=None):
        """
        Download a single image.

        Args:
            url: Image URL to download
            filename: Optional custom filename

        Returns:
            Path to saved file or None if download failed
        """
        # Skip if already downloaded
        url_hash = hashlib.md5(url.encode()).hexdigest()
        if url_hash in self.downloaded:
            return None

        try:
            response = self.session.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # Determine filename
            if not filename:
                # Extract filename from URL
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)

                # If no extension, try to get from content-type
                if '.' not in filename:
                    content_type = response.headers.get('content-type', '')
                    ext = '.jpg'  # default
                    if 'png' in content_type:
                        ext = '.png'
                    elif 'gif' in content_type:
                        ext = '.gif'
                    elif 'webp' in content_type:
                        ext = '.webp'
                    filename = f"image_{url_hash[:8]}{ext}"

            # Ensure unique filename
            filepath = os.path.join(self.output_dir, filename)
            counter = 1
            base, ext = os.path.splitext(filepath)
            while os.path.exists(filepath):
                filepath = f"{base}_{counter}{ext}"
                counter += 1

            # Save image
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.downloaded.add(url_hash)
            return filepath

        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return None

    def scrape_and_download(self, url, max_images=None, delay=0.5):
        """
        Scrape a webpage and download all images.

        Args:
            url: Webpage URL to scrape
            max_images: Maximum number of images to download (None for all)
            delay: Delay between downloads in seconds

        Returns:
            List of successfully downloaded file paths
        """
        print(f"Scraping images from: {url}")

        image_urls = self.get_image_urls(url)
        print(f"Found {len(image_urls)} images")

        if max_images:
            image_urls = image_urls[:max_images]

        downloaded_files = []

        for i, img_url in enumerate(image_urls, 1):
            print(f"Downloading [{i}/{len(image_urls)}]: {img_url[:50]}...")

            filepath = self.download_image(img_url)
            if filepath:
                downloaded_files.append(filepath)
                print(f"  Saved: {filepath}")

            time.sleep(delay)  # Be respectful

        print(f"\nDownloaded {len(downloaded_files)} images to '{self.output_dir}'")
        return downloaded_files


def demo_unsplash_source():
    """
    Demo using Unsplash Source (random images).
    This is a legitimate way to get free stock images.
    """
    print("\n" + "="*50)
    print("Unsplash Source Demo - Random Images")
    print("="*50)

    scraper = ImageScraper('unsplash_images')

    # Unsplash Source provides random images at specific URLs
    categories = ['nature', 'technology', 'architecture']

    for category in categories:
        # Note: This URL gives a random image each time
        url = f"https://source.unsplash.com/800x600/?{category}"

        print(f"\nDownloading random {category} image...")
        filepath = scraper.download_image(url, f"{category}_random.jpg")
        if filepath:
            print(f"Saved: {filepath}")

        time.sleep(1)


def demo_placeholder_images():
    """
    Demo downloading placeholder images (safe for testing).
    """
    print("\n" + "="*50)
    print("Placeholder Images Demo")
    print("="*50)

    scraper = ImageScraper('placeholder_images')

    # Download various placeholder images for testing
    placeholder_urls = [
        "https://via.placeholder.com/300x200/3498db/ffffff?text=Blue",
        "https://via.placeholder.com/300x200/e74c3c/ffffff?text=Red",
        "https://via.placeholder.com/300x200/2ecc71/ffffff?text=Green",
        "https://via.placeholder.com/300x200/f39c12/ffffff?text=Orange",
        "https://via.placeholder.com/300x200/9b59b6/ffffff?text=Purple",
    ]

    for i, url in enumerate(placeholder_urls, 1):
        filepath = scraper.download_image(url, f"placeholder_{i}.png")
        if filepath:
            print(f"Downloaded: {filepath}")
        time.sleep(0.5)


def main():
    """Main function demonstrating image scraping."""
    print("Image Scraper Demo")
    print("="*60)
    print("\nNote: Only scrape images from websites where you have")
    print("permission and always respect copyright laws.\n")

    # Demo 1: Scrape from a practice website
    print("="*50)
    print("Demo: Scraping from Books to Scrape")
    print("="*50)

    scraper = ImageScraper('books_images')
    downloaded = scraper.scrape_and_download(
        "http://books.toscrape.com/",
        max_images=5,
        delay=0.5
    )

    # Demo 2: Placeholder images
    demo_placeholder_images()

    print("\n" + "="*60)
    print("Image scraping demos complete!")
    print("\nRemember:")
    print("1. Always check robots.txt before scraping")
    print("2. Respect rate limits")
    print("3. Check copyright and terms of service")
    print("4. Consider using official APIs when available")


if __name__ == "__main__":
    main()
