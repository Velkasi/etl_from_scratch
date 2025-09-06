import pandas as pd
import re
import snowflake.connector
import numpy as np
from extract import OUTPUT_FILE
# Charger le fichier CSV généré par extract .py

df_all = pd.read_csv(OUTPUT_FILE)


con = snowflake.connector.connect(
        account = "XXXXXXXXX",
        user = "XXXXXXXXX",
        password = "XXXXXXXX",
        role = "ACCOUNTADMIN",
        warehouse = "COMPUTE_WH",
        database = "SCRAPPING_PROJECT",
        schema = "RAW",
        session_parameters={
            'QUERY_TAG': 'scrapping_data_load',
        }
)

# Initier la connexion avec SnowFlake et créer la table (BDD créer au préalable)
cs = con.cursor()

cs.execute("""CREATE TABLE IF NOT EXISTS  SCRAPPING_RAW (
timestamp TIMESTAMP_NTZ,
author VARCHAR(16777216),
country VARCHAR(16777216),
author_reviews_count INT,
rating INT,
text VARCHAR(16777216),
date TIMESTAMP_NTZ,
url VARCHAR(16777216)
)
""")

# Charger dans Snowflake

for _, row in df_all.iterrows():

    author_reviews_count_value = None
    if pd.notnull(row['author_reviews_count']):
        match = re.search(r'\d+', str(row['author_reviews_count']))
        if match:
            author_reviews_count_value = int(match.group())

    author = row['author'] if pd.notnull(row['author']) else None
    country = row['country'] if pd.notnull(row['country']) else None
    rating = int(row['rating']) if pd.notnull(row['rating']) else None
    text = row['text'] if pd.notnull(row['text']) else None
    date = pd.to_datetime(row['date']).strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row['date']) else None
    url = row['url'] if pd.notnull(row['url']) else None

    cs.execute(
        "INSERT INTO SCRAPPING_RAW (timestamp, author, country, author_reviews_count, rating, text, date, url) "
        "VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s)",
        (
            author,
            country,
            author_reviews_count_value,
            rating,
            text,
            date,
            url
        )
    )

con.commit() # Valide les changements
cs.close() # Ferme le curseur
con.close() # Ferme la connexion