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
    Fetches stock market data and fundamental financial indicators for a given list of tickers.
    """
    ticker_obj = Ticker(tickers)

    # Fetch data from Yahoo Finance
    summary = ticker_obj.summary_detail  # Market price, daily high/low, volume, market cap
    key_stats = ticker_obj.key_stats  # P/E Ratio, Beta, Market Cap
    financials = ticker_obj.financial_data  # EBITDA, Free Cash Flow, Debt Ratios
    valuation_measures = ticker_obj.valuation_measures  # EV/EBITDA, Price/Book
    price_history = ticker_obj.history(period="1y")  # 1-year historical price data

    records = []
    for symbol in tickers:
        data = {
            # Stock Market Data
            "symbol": symbol,
            "market_price": summary.get(symbol, {}).get("regularMarketPrice"),
            "market_change": summary.get(symbol, {}).get("regularMarketChange"),
            "market_change_percent": summary.get(symbol, {}).get("regularMarketChangePercent"),
            "market_high": summary.get(symbol, {}).get("regularMarketDayHigh"),
            "market_low": summary.get(symbol, {}).get("regularMarketDayLow"),
            "market_volume": summary.get(symbol, {}).get("regularMarketVolume"),
            "market_cap": key_stats.get(symbol, {}).get("marketCap"),

            # Financial Ratios
            "pe_ratio": key_stats.get(symbol, {}).get("trailingPE"),  # Price-to-Earnings Ratio
            "forward_pe": key_stats.get(symbol, {}).get("forwardPE"),
            "pb_ratio": valuation_measures.get(symbol, {}).get("priceToBook"),  # Price-to-Book Ratio
            "ev_ebitda": valuation_measures.get(symbol, {}).get("enterpriseToEbitda"),  # EV/EBITDA
            
            # Profitability & Cash Flow
            "ebitda": financials.get(symbol, {}).get("ebitda"),
            "operating_margin": financials.get(symbol, {}).get("operatingMargins"),
            "gross_margin": financials.get(symbol, {}).get("grossMargins"),
            "free_cash_flow": financials.get(symbol, {}).get("freeCashflow"),

            # Debt & Risk Indicators
            "debt_to_equity": financials.get(symbol, {}).get("debtToEquity"),
            "current_ratio": financials.get(symbol, {}).get("currentRatio"),
            "beta": key_stats.get(symbol, {}).get("beta"),

            # Dividend & Shareholder Returns
            "dividend_yield": financials.get(symbol, {}).get("dividendYield"),
            "payout_ratio": financials.get(symbol, {}).get("payoutRatio"),

            # Stock Performance (1-Year Data)
            "yearly_high": price_history.loc[symbol].high.max() if symbol in price_history.index else None,
            "yearly_low": price_history.loc[symbol].low.min() if symbol in price_history.index else None,
            "yearly_return": ((summary.get(symbol, {}).get("regularMarketPrice", 1) / 
                               price_history.loc[symbol].close.iloc[0]) - 1) * 100 if symbol in price_history.index else None,

            "date_collected": pd.Timestamp.now()
        }
        records.append(data)

    return pd.DataFrame(records)

# 🔹 Écrire les données dans BigQuery
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

# 🔹 Exécution du pipeline
if __name__ == "__main__":
    print("🚀 Fetching stock data...")
    stock_df = fetch_stock_data(["AAPL", "TSLA", "GOOGL"])  # Ajoute tes tickers ici

    print("🚀 Uploading data to BigQuery...")
    write_to_bigquery(stock_df)

    print("✅ Done!")