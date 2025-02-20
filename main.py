import os
import pandas as pd
from yahooquery import Ticker
from google.cloud import bigquery

# Configuration des variables
YAHOO_TICKERS = ["AAPL", "TSLA", "GOOGL"]  # Ajoute les actions que tu veux suivre
BIGQUERY_PROJECT_ID = "quiet-dimension-427207-t0"  # Remplace par ton ID de projet GCP
BIGQUERY_DATASET = "investor_dashboard"
BIGQUERY_TABLE = "stock_prices"

import os
import pandas as pd
from yahooquery import Ticker
from google.cloud import bigquery

# 🔹 Configuration
BIGQUERY_PROJECT_ID = "quiet-dimension-427207-t0"  # Remplace avec ton ID de projet
BIGQUERY_DATASET = "investor_dashboard"
BIGQUERY_TABLE = "stock_prices"

# Initialise le client BigQuery
client = bigquery.Client()

# 🔹 Fetch Stock Market Data & Key Financial Indicators
def fetch_stock_data(tickers):
    """
    Fetches all available stock data in a single API call and structures it into a DataFrame.
    """
    ticker_obj = Ticker(tickers)
    raw_data = ticker_obj.all_modules  # Retrieve full JSON for all tickers

    records = []
    for symbol in tickers:
        info = raw_data.get(symbol, {})

        data = {
            "symbol": symbol,
            "market_price": info.get("price", {}).get("regularMarketPrice"),
            "market_cap": info.get("price", {}).get("marketCap"),
            "pe_ratio": info.get("summaryDetail", {}).get("trailingPE"),
            "forward_pe": info.get("defaultKeyStatistics", {}).get("forwardPE"),
            "pb_ratio": info.get("defaultKeyStatistics", {}).get("priceToBook"),
            "ev_ebitda": info.get("defaultKeyStatistics", {}).get("enterpriseToEbitda"),
            "ebitda": info.get("financialData", {}).get("ebitda"),
            "free_cash_flow": info.get("financialData", {}).get("freeCashflow"),
            "debt_to_equity": info.get("financialData", {}).get("debtToEquity"),
            "operating_margin": info.get("financialData", {}).get("operatingMargins"),
            "gross_margin": info.get("financialData", {}).get("grossMargins"),
            "current_ratio": info.get("financialData", {}).get("currentRatio"),
            "beta": info.get("defaultKeyStatistics", {}).get("beta"),
            "dividend_yield": info.get("summaryDetail", {}).get("dividendYield"),
            "payout_ratio": info.get("summaryDetail", {}).get("payoutRatio"),
            "yearly_high": info.get("summaryDetail", {}).get("fiftyTwoWeekHigh"),
            "yearly_low": info.get("summaryDetail", {}).get("fiftyTwoWeekLow"),
            "date_collected": pd.Timestamp.now()
        }

        records.append(data)

    return pd.DataFrame(records)

# 🔹 Écrire les données dans BigQuery
def write_to_bigquery(df):
    """
    Uploads a DataFrame to BigQuery after user confirmation.
    """
    if df.empty:
        print("⚠️ No data to upload!")
        return

    # 🔍 Display sample data for validation
    print("🔍 Checking DataFrame before inserting into BigQuery:")
    print(df.head())  # Display the first rows of the DataFrame

    # ✅ Ask for confirmation before uploading
    confirm = input("✅ Do you want to upload this data to BigQuery? (Yes/No): ").strip().lower()
    if confirm != "yes":
        print("❌ Upload canceled by user.")
        return

    table_id = f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"✅ Successfully uploaded {len(df)} rows to {table_id}")
    except Exception as e:
        print(f"❌ Error uploading data: {e}")
        
# 🔹 Exécution du pipeline
if __name__ == "__main__":
    print("🚀 Fetching stock data...")
    stock_df = fetch_stock_data(["AAPL", "TSLA", "GOOGL"])  # Ajoute tes tickers ici

    print("🚀 Uploading data to BigQuery...")
    write_to_bigquery(stock_df)

    print("✅ Done!")