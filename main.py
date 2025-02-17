import os
import pandas as pd
from yahooquery import Ticker
from google.cloud import bigquery

# Configuration des variables
YAHOO_TICKERS = ["AAPL", "TSLA", "GOOGL"]  # Ajoute les actions que tu veux suivre
BIGQUERY_PROJECT_ID = "quiet-dimension-427207-t0"  # Remplace par ton ID de projet GCP
BIGQUERY_DATASET = "investor_dashboard"
BIGQUERY_TABLE = "stock_prices"

# Initialisation du client BigQuery
client = bigquery.Client()

# Fonction pour récupérer les prix des actions via Yahoo Finance
def fetch_stock_data(tickers):
    """
    Récupère les prix des actions et retourne un DataFrame formaté.
    """
    ticker_obj = Ticker(tickers)
    data = ticker_obj.price  # Récupère les données de marché

    records = []
    for symbol, info in data.items():
        records.append({
            "symbol": symbol,
            "market_price": info.get("regularMarketPrice"),
            "market_change": info.get("regularMarketChange"),
            "market_high": info.get("regularMarketDayHigh"),
            "market_low": info.get("regularMarketDayLow"),
            "market_volume": info.get("regularMarketVolume"),
            "market_time": info.get("regularMarketTime")
        })

    return pd.DataFrame(records)

# Fonction pour écrire les données dans BigQuery
def write_to_bigquery(df):
    """
    Envoie un DataFrame dans BigQuery.
    """
    if df.empty:
        print("⚠️ No data to upload!")
        return

    table_id = f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Attendre la fin du job
        print(f"✅ Successfully uploaded {len(df)} rows to {table_id}")
    except Exception as e:
        print(f"❌ Error uploading data: {e}")

# Exécution du pipeline
if __name__ == "__main__":
    print("🚀 Fetching stock data...")
    stock_df = fetch_stock_data(YAHOO_TICKERS)

    print("🚀 Uploading data to BigQuery...")
    write_to_bigquery(stock_df)

    print("✅ Done!")