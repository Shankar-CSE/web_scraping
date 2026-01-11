# Web Scraping Examples 🕸️

A collection of web scraping projects, ideas, and practice code using Python. This repository serves as a reference for learning and implementing various web scraping techniques.

## 📋 Table of Contents

- [Features](#features)
- [Projects](#projects)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- Practical web scraping examples
- Clean and well-documented code
- Uses modern Python libraries
- Jupyter notebooks for interactive learning
- Reusable utility functions

## 📁 Projects

### 1. Wikipedia Companies Scraper (`wikipedia.ipynb`)

Scrapes the list of largest companies in the United States by revenue from Wikipedia.

- Parses HTML tables using BeautifulSoup
- Exports data to CSV format
- **Output:** `output.csv`

### 2. Quotes Scraper (`quotes_scraper.ipynb`)

Scrapes quotes from [Quotes to Scrape](http://quotes.toscrape.com/).

- Basic HTML parsing
- Multi-page pagination handling
- Extracts quotes, authors, and tags
- **Output:** `quotes_output.csv`

### 3. Books Scraper (`books_scraper.ipynb`)

Scrapes book data from [Books to Scrape](http://books.toscrape.com/).

- Product listing extraction
- Price and rating parsing
- Handles relative URLs
- **Output:** `books_output.csv`

### 4. News Scraper (`news_scraper.py`)

Command-line tool to scrape stories from Hacker News.

- CLI interface with arguments
- JSON and CSV export options
- Score and comment tracking
- **Output:** `hacker_news.csv` / `hacker_news.json`

### 5. API Scraper (`api_scraper.py`)

Demonstrates fetching data from public APIs.

- REST API requests
- JSON response handling
- Rate limiting
- GitHub and JSONPlaceholder APIs
- **Output:** `api_posts.csv`, `github_repos.csv`

### 6. Image Scraper (`image_scraper.py`)

Downloads images from websites.

- Image URL extraction
- Bulk downloading with progress
- Organized output directories
- **Output:** `downloaded_images/`

### 7. Utility Module (`utils/`)

Reusable scraper utilities.

- Base scraper class
- User-Agent rotation
- Retry decorators
- Text cleaning functions
- Export helpers

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Shankar-CSE/web_scraping.git
   cd web_scraping
   ```

2. **Create a virtual environment**

   ```bash
   # On Linux/Mac
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Jupyter Notebooks

Open any notebook in Jupyter or VS Code:

```bash
jupyter notebook quotes_scraper.ipynb
```

### Python Scripts

**News Scraper:**

```bash
# Scrape 1 page (default)
python news_scraper.py

# Scrape multiple pages
python news_scraper.py -p 3

# Export as JSON
python news_scraper.py -p 2 -o json

# Custom filename
python news_scraper.py -p 5 -f my_news_data
```

**API Scraper:**

```bash
python api_scraper.py
```

**Image Scraper:**

```bash
python image_scraper.py
```

### Using Utility Functions

```python
from utils import BaseScraper, clean_text, save_to_csv

# Create a scraper with rate limiting
scraper = BaseScraper("https://example.com", rate_limit=1.0)

# Fetch and parse a page
soup = scraper.fetch("/page")

# Clean extracted text
text = clean_text(soup.find('p').text)

# Save results
save_to_csv(data, 'output.csv')
```

## 🛠️ Technologies

| Library            | Purpose                    |
| ------------------ | -------------------------- |
| **BeautifulSoup4** | HTML/XML parsing           |
| **Requests**       | HTTP requests              |
| **Pandas**         | Data manipulation & export |
| **lxml**           | Fast HTML/XML parser       |

## 📂 Project Structure

```
web_scraping/
├── wikipedia.ipynb       # Wikipedia companies scraper
├── quotes_scraper.ipynb  # Quotes to Scrape scraper
├── books_scraper.ipynb   # Books to Scrape scraper
├── news_scraper.py       # Hacker News CLI scraper
├── api_scraper.py        # API data fetcher
├── image_scraper.py      # Image downloader
├── utils/
│   ├── __init__.py
│   └── scraper_utils.py  # Reusable utilities
├── requirements.txt
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── CODE_OF_CONDUCT.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

Always respect website terms of service and robots.txt files when scraping:

- Rate limit your requests
- Don't overload servers
- Follow copyright and data usage policies
- Use official APIs when available

## 📧 Contact

Shankar-CSE - [@Shankar-CSE](https://github.com/Shankar-CSE)

Project Link: [https://github.com/Shankar-CSE/web_scraping](https://github.com/Shankar-CSE/web_scraping)
