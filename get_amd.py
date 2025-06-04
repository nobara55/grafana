import yfinance as yf
data = yf.download("AMD", period="5d", progress=False)
data.to_csv("amd_stock_data.csv")
print("Done")
