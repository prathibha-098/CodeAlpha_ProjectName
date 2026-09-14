import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

st.set_page_config(page_title="CodeAlpha Task 1 - Web Scraping", layout="wide")
st.title("🕷️ Task 1 — Web Scraping")
st.caption("Extract structured book data from Books to Scrape using Requests + BeautifulSoup.")

DEFAULT_URL = "https://books.toscrape.com/"

def scrape_books(url, max_pages=3):
    rows = []
    for page in range(1, max_pages + 1):
        page_url = url.rstrip("/") + ("/catalogue/page-{}.html".format(page) if page == 1 else "/catalogue/page-{}.html".format(page))
        r = requests.get(page_url, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.select("article.product_pod"):
            title = card.h3.a.get("title", "").strip()
            price = card.select_one(".price_color").get_text(strip=True)
            availability = card.select_one(".availability").get_text(" ", strip=True)
            rating = " ".join(card.get("class", []))
            rows.append({"title": title, "price": price, "availability": availability, "rating_class": rating, "source_page": page})
    return pd.DataFrame(rows)

st.sidebar.header("Scraper settings")
url = st.sidebar.text_input("Website URL", DEFAULT_URL)
pages = st.sidebar.slider("Pages to scrape", 1, 5, 2)
run = st.sidebar.button("🚀 Start scraping", type="primary")

st.info("This demo uses the public practice site Books to Scrape. It is designed for learning HTML parsing and dataset creation.")

if run:
    try:
        df = scrape_books(url, pages)
        st.success(f"Collected {len(df)} records from {pages} page(s).")
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download CSV", df.to_csv(index=False), "scraped_books.csv", "text/csv")
        st.subheader("Quick summary")
        c1,c2,c3 = st.columns(3)
        c1.metric("Records", len(df))
        c2.metric("Unique titles", df["title"].nunique())
        c3.metric("Pages", df["source_page"].nunique())
    except Exception as e:
        st.error("Scraping failed. Check your internet connection and URL.")
        st.exception(e)
else:
    st.markdown("### What this demonstrates")
    st.markdown("- Sends an HTTP request with `requests`.\n- Parses HTML with `BeautifulSoup`.\n- Extracts title, price, availability and rating information.\n- Converts the results into a pandas DataFrame.\n- Exports a custom CSV dataset.")
