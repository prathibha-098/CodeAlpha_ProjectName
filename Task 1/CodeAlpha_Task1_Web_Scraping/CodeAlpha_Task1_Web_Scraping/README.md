# CodeAlpha Task 1 — Web Scraping

## Requirement covered
The CodeAlpha brief asks interns to use Python libraries such as BeautifulSoup/Scrapy to extract relevant data from public web pages and create custom datasets.

## Stack
- Frontend: Streamlit UI
- Backend: Python scraper
- Parsing: BeautifulSoup
- HTTP: Requests
- Data handling: Pandas

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit.

## Output
The app displays scraped records and lets you download `scraped_books.csv`.

## Internship explanation
"I built a web-scraping application that sends HTTP requests to a public practice website, parses the HTML structure with BeautifulSoup, extracts book attributes, stores them in a pandas DataFrame, and exports the collected data as CSV."
