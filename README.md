**📊 Investor Dashboard - Real-Time Stock Market Insights**



**📌 Project Overview**

Investor Dashboard is a real-time business intelligence tool designed to showcase ETL and workflow automation skills to potential recruiters. This project integrates various financial data sources, processes them using modern data engineering tools, and presents insights through an interactive dashboard.



**🎯 Key Features**

Real-time stock price tracking using Yahoo Finance API

Financial metrics calculation (P/E ratio, EBITDA, Free Cash Flow, etc.)

Automated data pipeline with Python, BigQuery, and dbt

Interactive visualizations via Looker Studio or Streamlit



**📂 Project Structure**

📦 investor-dashboard
 ├── 📂 data                 # Sample datasets (temporary storage)

 ├── 📂 scripts              # Python scripts for data extraction

 ├── 📂 dbt                  # dbt transformations and models

 ├── 📂 dashboard            # Looker Studio or Streamlit dashboard

 ├── 📂 docs                 # Project documentation

 ├── 📜 requirements.txt     # List of dependencies

 ├── 📜 README.md            # Project overview

 ├── 📜 .gitignore           # Files to exclude from Git



**🔗 Data Sources**

Yahoo Finance API (Stock prices, historical data)

Alpha Vantage (Stock market data, fundamental analysis)

SEC EDGAR Database (US company financial filings)



**🚀 Tech Stack**

ETL & Data Processing: Python, YahooQuery, Pandas

Data Storage: Google BigQuery

Data Transformation: dbt (Data Build Tool)

Dashboard & Visualization: Looker Studio / Streamlit



**🏗️ Installation & Setup**

Clone the repository

git clone https://github.com/your-username/investor-dashboard.git
cd investor-dashboard

Set up a virtual environment

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Configure API keys (Replace with your own keys)

export YAHOO_API_KEY='your_yahoo_api_key'
export ALPHA_VANTAGE_KEY='your_alpha_vantage_key'

Run the first data extraction script

python scripts/fetch_stock_prices.py



**📊 Data Pipeline Workflow**

Extract: Retrieve stock prices and financial metrics via APIs

Load: Store raw data in Google BigQuery

Transform: Use dbt to compute financial ratios and KPIs

Visualize: Build an interactive dashboard using Looker Studio or Streamlit



**📅 Roadmap**

✅ Set up initial data pipeline

✅ Implement data extraction scripts (Yahoo Finance, Alpha Vantage)

🔲 Automate data ingestion to BigQuery

🔲 Create dbt transformations for KPI calculations

🔲 Develop a real-time dashboard (Looker Studio / Streamlit)

🔲 Deploy the project for public access



**🏆 Author**

Vincent Lamy - [GitHub](https://github.com/Vincent-20-100) - [LinkedIn](https://www.linkedin.com/in/42-v-lamy/)



**📜 License**

This project is licensed under the MIT License - see the LICENSE file for details.

Vincent Lamy - GitHub - LinkedIn

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
