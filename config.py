from yahooquery import Ticker
!pip install ace_tools

ticker = Ticker("AAPL")
print(ticker.price)