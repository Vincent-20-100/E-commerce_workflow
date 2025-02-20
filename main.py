import os
import pandas as pd
from yahooquery import Ticker
from google.cloud import bigquery

# Configuration des variables
YAHOO_TICKERS = ["AAPL", "TSLA", "GOOGL"]  # Ajoute les actions que tu veux suivre
BIGQUERY_PROJECT_ID = "quiet-dimension-427207-t0"  # Remplace par ton ID de projet GCP
BIGQUERY_DATASET = "investor_dashboard"
BIGQUERY_TABLE = "stock_prices"

CAC40_TICKERS = [
    "AC.PA", "AI.PA", "AIR.PA", "AKE.PA", "ALO.PA", "AM.PA", "ATO.PA", "BEN.PA", "BN.PA", "BNP.PA",
    "BOUY.PA", "CAP.PA", "CS.PA", "DG.PA", "DSY.PA", "EL.PA", "EN.PA", "ENGI.PA", "ERM.PA", "HO.PA",
    "KER.PA", "LR.PA", "MC.PA", "ML.PA", "OR.PA", "ORA.PA", "PUB.PA", "RMS.PA", "RI.PA", "SAF.PA",
    "SAN.PA", "SGO.PA", "STM.PA", "SU.PA", "TTE.PA", "VIE.PA", "VIV.PA", "WLN.PA"
]

# 🔹 Configuration
BIGQUERY_PROJECT_ID = "quiet-dimension-427207-t0"  # Remplace avec ton ID de projet
BIGQUERY_DATASET = "investor_dashboard"
BIGQUERY_TABLE = "stock_prices"

# Initialise le client BigQuery
client = bigquery.Client()

# 🔹 Fetch Stock Market Data & Key Financial Indicators
def fetch_stock_data(tickers):
    """
    Fetches financial and market data for a list of tickers from Yahoo Finance.
    """
    ticker_obj = Ticker(tickers)
    raw_data = ticker_obj.all_modules  # Retrieve full JSON for all tickers

    records = []
    for symbol in tickers:
        info = raw_data.get(symbol, {})

        # ✅ Ensure `info` is a dictionary before processing
        if not isinstance(info, dict):
            print(f"⚠️ Skipping {symbol} - Unexpected response: {info}")
            continue  

        data = {
            "symbol": symbol,
            "market_price": info.get("price", {}).get("regularMarketPrice", None),
            "market_cap": info.get("price", {}).get("marketCap", None),
            "pe_ratio": info.get("summaryDetail", {}).get("trailingPE", None),
            "forward_pe": info.get("defaultKeyStatistics", {}).get("forwardPE", None),
            "pb_ratio": info.get("defaultKeyStatistics", {}).get("priceToBook", None),
            "ev_ebitda": info.get("defaultKeyStatistics", {}).get("enterpriseToEbitda", None),
            "ebitda": info.get("financialData", {}).get("ebitda", None),
            "free_cash_flow": info.get("financialData", {}).get("freeCashflow", None),
            "debt_to_equity": info.get("financialData", {}).get("debtToEquity", None),
            "operating_margin": info.get("financialData", {}).get("operatingMargins", None),
            "gross_margin": info.get("financialData", {}).get("grossMargins", None),
            "current_ratio": info.get("financialData", {}).get("currentRatio", None),
            "beta": info.get("defaultKeyStatistics", {}).get("beta", None),
            "dividend_yield": info.get("summaryDetail", {}).get("dividendYield", None),
            "payout_ratio": info.get("summaryDetail", {}).get("payoutRatio", None),
            "yearly_high": info.get("summaryDetail", {}).get("fiftyTwoWeekHigh", None),
            "yearly_low": info.get("summaryDetail", {}).get("fiftyTwoWeekLow", None),
            "sector": info.get("assetProfile", {}).get("sector", None),
            "industry": info.get("assetProfile", {}).get("industry", None),
            "total_revenue": info.get("financialData", {}).get("totalRevenue", None),
            "revenue_growth": info.get("financialData", {}).get("revenueGrowth", None),
            "profit_margins": info.get("financialData", {}).get("profitMargins", None),
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
    print("🚀 Fetching CAC 40 stock data...")

    # 🔹 Utiliser la liste complète du CAC 40
    selected_tickers = CAC40_TICKERS
    print(f"\n📊 Fetching data for CAC 40")

    # Fetch CAC 40 stock data
    stock_df = fetch_stock_data(CAC40_TICKERS)

    # Display the first rows to check the data
    print(stock_df.head())


    print("🚀 Ready to upload CAC 40 data to BigQuery...")
    write_to_bigquery(stock_df)

    print("✅ Done!")