import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import datetime
from scrapingbee import ScrapingBeeClient
from fastapi import FastAPI
import json


#Creation des variables pour l'api ScrapingBee
API_KEY = ScrapingBeeClient(api_key='CTDMUER0L7R1ZDPZ9YU9YO7U6SRDNH1NL12VYJ8X79THY5F2ST6IC3LZIMYFSQRSJR7TNZ5QCVBQS5TH')
URL = "https://fr.trustpilot.com/review/www.intersport.fr"

#Requete a l'api ScrapingBee
response = API_KEY.get(
    URL,
    params = { 
         'wait': '5000',
         'block_ads': 'True',
         'ai_selector': "avis",
         'json_response': 'True',
    }
)

print('Reponse HTTP Status Code:', response.status_code)
print('Response HTTP Reponse Body:', response.content)


# Enregistrement des donnees dans un fichier JSON
if response.status_code == 200:
    new_data = response.json()
    try:
        with open("data.json", "r") as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    existing_data.append(new_data)

    with open("data.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
        print("Data appended to data.json file.")
else:
    print("Failed to retrieve data from the API. Status code:", response.status_code)


# Données a fetch
'''

"@type": "Review",
                            "@id": "https://www.trustpilot.com/#/schema/Review/www.intersport.fr/68b9620706358ae26b8a20fe",
                            "itemReviewed": {
                                "@id": "https://www.trustpilot.com/#/schema/Organization/www.intersport.fr"
                            },
                            "author": {
                                "@type": "Person",
                                "name": "Wafa KHOUILDI",
                                "url": "https://fr.trustpilot.com/users/67eea4ad25760184a896d349/"
                            },
                            "datePublished": "2025-09-04T11:55:19.000Z",
                            "headline": "J\u2019ai pu trouv\u00e9 la paire que je cherche\u2026",
                            "reviewBody": "J\u2019ai pu trouv\u00e9 la paire que je cherche depuis un moment, elle \u00e9tait toujours en rupture et en plus je l\u2019ai eu \u00e0 -40%. Livraison tr\u00e8s rapide en moins de 48h je l\u2019ai re\u00e7u. Merci INTERSPORT",
                            "reviewRating": {
                                "@type": "Rating",
                                "bestRating": "5",
                                "worstRating": "1",
                                "ratingValue": "5"

'''
# def fetch_html(url)
    



# parse_reviews(html)




# to_dataframe(reviews)