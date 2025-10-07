# scraper.py
# Polite same-domain crawler for docs.capillarytech.com
import os, time, json
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

BASE_URL = os.getenv("BASE_URL", "https://docs.capillarytech.com/")
OUT_FILE = "data/docs.jsonl"
RAW_DIR = "data/raw"

os.makedirs(RAW_DIR, exist_ok=True)

session = requests.Session()
session.headers.update({"User-Agent":"capillary-docs-scraper/1.0 (you@example.com)"})

def same_domain(url):
    return urlparse(url).netloc.endswith(urlparse(BASE_URL).netloc)

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["nav","footer","script","style","aside","noscript","svg"]):
        tag.decompose()
    article = soup.find("main") or soup.find("article") or soup
    title = soup.title.string.strip() if soup.title else ""
    parts = []
    for el in article.find_all(["h1","h2","h3","p","li"]):
        t = el.get_text(separator=" ", strip=True)
        if t:
            parts.append(t)
    return title, "\n\n".join(parts)

def crawl(start):
    q = [start]
    visited = set()
    docs = []
    while q:
        url = q.pop(0)
        if url in visited: 
            continue
        visited.add(url)
        try:
            r = session.get(url, timeout=15)
            if r.status_code != 200:
                # skip non-200
                continue
            title, text = extract_text(r.text)
            if text.strip():
                docs.append({"url": url, "title": title, "text": text})
                # save raw html optionally
                safe_name = url.replace("https://","").replace("http://","").replace("/","_")
                fname = os.path.join(RAW_DIR, safe_name + ".html")
                with open(fname, "w", encoding="utf-8") as fh:
                    fh.write(r.text)
                print(f"Scraped: {url} ({len(text)} chars)")
            # find same-domain links
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a['href'].split('#')[0]
                full = urljoin(url, href)
                if same_domain(full) and full not in visited and full not in q:
                    q.append(full)
            time.sleep(0.5)
        except Exception as e:
            print("Error", url, e)
    # write docs.jsonl
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    print(f"✅ Scraped {len(docs)} pages -> {OUT_FILE}")

if __name__ == "__main__":
    crawl(BASE_URL)
