import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import datetime
from scrapingbee import ScrapingBeeClient



#Creation des variables pour l'api ScrapingBee
API_KEY = ScrapingBeeClient(api_key='CTDMUER0L7R1ZDPZ9YU9YO7U6SRDNH1NL12VYJ8X79THY5F2ST6IC3LZIMYFSQRSJR7TNZ5QCVBQS5TH')

response = API_KEY.get("https://fr.trustpilot.com/review/www.intersport.fr")

print('Reponse HTTP Status Code:', response.status_code)
print('Response HTTP Reponse Body:', response.content)

# def fetch_html(url)
    



# parse_reviews(html)




# to_dataframe(reviews)