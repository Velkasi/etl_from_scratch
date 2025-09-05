import pandas as pd
import re
import snowflake.connector
from extract import OUTPUT_FILE
# Charger le fichier CSV généré par extract .py

#df = '.reviews_all_pages.csv'  # Chemin vers le fichier CSV
df_all = pd.read_csv(OUTPUT_FILE)


con = snowflake.connector.connect(
        account = "XXXXXXX",
        user = "XXXXX",
        authenticator = "externalbrowser",
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

cs.execute("""CREATE OR REPLACE TABLE SCRAPPING_RAW (
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
    cs.execute(
        "INSERT INTO SCRAPPING_RAW (timestamp, author, country, author_reviews_count, rating, text, date, url) "
        "VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s)",
        (
        row['author'],
        row['country'],
        int(re.search(r'\d+', row['author_reviews_count']).group()) if row['author_reviews_count'] else None,
        row['rating'],
        row['text'],
        pd.to_datetime(row['date']).strftime('%Y-%m-%d %H:%M:%S') if row['date'] else None,
        row['url']
        )
    )

con.commit() # Valide les changements
cs.close() # Ferme le curseur
con.close() # Ferme la connexion