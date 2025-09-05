import requests
from bs4 import BeautifulSoup
import snowflake.connector
import pandas as pd
import re
from pathlib import Path

API_KEY = "CTDMUER0L7R1ZDPZ9YU9YO7U6SRDNH1NL12VYJ8X79THY5F2ST6IC3LZIMYFSQRSJR7TNZ5QCVBQS5TH"  # ton token ScrapingBee ou autre proxy pour eviter le ban !
URL = "https://fr.trustpilot.com/review/www.decathlon.fr" # Tu peux choisir celui que tu souhaite
OUTPUT_FILE = Path(r'./reviews_all_pages.csv') # Mon chemin pour debugg et log

def get_reviews(url):
    """
    Scrape les avis d'une seule page Trustpilot.
    """
    js_scenario = {
        "instructions": [
            {"scroll_y": 2000},
            {"wait": 2000},
            {"scroll_y": 4000},
            {"wait": 2000}
        ]
    }

    response = requests.get(
        "https://app.scrapingbee.com/api/v1/",
        params={
            "api_key": API_KEY,
            "url": url,
            "render_js": "true",
            "js_scenario": str(js_scenario),
            "wait": "5000",
            "block_ads": "true"
        },
    )

    soup = BeautifulSoup(response.text, "html.parser")

    reviews_data = []
    reviews = soup.select("article")  # chaque avis est dans un <article>

		# Pour cette partie, il faut ce rendre sur le site web directement est regarder les balises qu'on souhaite.
    for r in reviews:
        author = r.select_one("[data-consumer-name-typography]")
        country = r.select_one("[data-consumer-country-typography]")
        author_reviews_count = r.select_one("[data-consumer-reviews-count-typography]")
        rating = r.select_one("img[alt*='étoiles']")
        text = r.select_one("p[data-service-review-text-typography]")
        date = r.select_one("time")

        # Extraction de la note
        note = None
        if rating and "alt" in rating.attrs:
            match = re.search(r"(\d+)", rating["alt"])
            if match:
                note = int(match.group(1))

        reviews_data.append({
            "author": author.get_text(strip=True) if author else None,
            "country": country.get_text(strip=True) if country else None,
            "author_reviews_count": author_reviews_count.get_text(strip=True) if author_reviews_count else None,
            "rating": note,
            "text": text.get_text(strip=True) if text else None,
            "date": date["datetime"] if date else None,
            "url": url
        })

    df = pd.DataFrame(reviews_data)
    df['timestamp'] = pd.Timestamp.now()
    return df

if __name__ == "__main__":
    all_reviews = []

    NUM_PAGES = 5  # !!! AJUSTER selon le nombre d'avis que tu veux récupérer !!!
    for page in range(1, NUM_PAGES + 1):
        page_url = f"{URL}?page={page}"
        print(f"Scraping page {page}...")
        df_page = get_reviews(page_url)
        all_reviews.append(df_page)

    # Concaténer toutes les pages dans 1 dataframe
    df_all = pd.concat(all_reviews, ignore_index=True)

    # Créer le dossier si nécessaire
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Sauvegarder CSV
    df_all.to_csv(OUTPUT_FILE, index=False) 
    print(f"Avis récup : {len(df_all)}") # Verification du nombre d'avis
    print(df_all.head()) # Debug (print les 5 premier avis)
