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

## 📁 Projects

### Wikipedia Companies Scraper
A scraper that extracts the list of largest companies in the United States by revenue from Wikipedia.

**Features:**
- Parses HTML tables using BeautifulSoup
- Exports data to CSV format
- Handles data cleaning and formatting

**Output:** `output.csv` containing company revenue data

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

### Running the Wikipedia Scraper

Open and run the Jupyter notebook:
```bash
jupyter notebook wikipedia.ipynb
```

Or run it in VS Code with the Jupyter extension installed.

The script will:
1. Fetch data from Wikipedia
2. Parse the HTML table
3. Export results to `output.csv`

## 🛠️ Technologies

- **BeautifulSoup4** - HTML/XML parsing
- **Requests** - HTTP library for making requests
- **Pandas** - Data manipulation and CSV export

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

Always respect website terms of service and robots.txt files when scraping. Be mindful of:
- Rate limiting your requests
- Not overloading servers
- Following copyright and data usage policies

## 📧 Contact

Shankar-CSE - [@Shankar-CSE](https://github.com/Shankar-CSE)

Project Link: [https://github.com/Shankar-CSE/web_scraping](https://github.com/Shankar-CSE/web_scraping) 
