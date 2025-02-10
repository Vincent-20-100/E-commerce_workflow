import pyarrow
import requests
import pandas as pd
from google.cloud import bigquery

# Initialiser le client BigQuery
client = bigquery.Client()

# Définir les URLs de l'API Fake Store
PRODUCTS_URL = "https://fakestoreapi.com/products"
ORDERS_URL = "https://fakestoreapi.com/carts"

# Définir le dataset et les tables BigQuery
DATASET_ID = 'quiet-dimension-427207-t0.ecommerce_workflow'
TABLE_PRODUCTS = f"{DATASET_ID}.products"
TABLE_ORDERS = f"{DATASET_ID}.orders"

def fetch_data(url):
    """Récupère les données d'une API et les retourne sous forme de DataFrame"""
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        raise Exception(f"Erreur lors de la récupération des données : {response.status_code}")

def upload_to_bigquery(df, table_id):
    """Charge un DataFrame Pandas dans une table BigQuery"""
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Attendre la fin du job
    print(f"Données chargées dans {table_id}")

def main():
    print("Récupération des données...")
    
    # Récupération des produits
    df_products = fetch_data(PRODUCTS_URL)
    
    # Récupération des commandes
    df_orders = fetch_data(ORDERS_URL)

    print("Chargement des données dans BigQuery...")
    
    # Upload des produits
    upload_to_bigquery(df_products, TABLE_PRODUCTS)
    
    # Upload des commandes
    upload_to_bigquery(df_orders, TABLE_ORDERS)

    print("✅ Données importées avec succès dans BigQuery !")

if __name__ == "__main__":
    main()