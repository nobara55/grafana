import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def fetch_and_save_amd_data():
    ticker = "AMD"
    today = datetime.today().date()
    file_path = "amd_stock_data.csv"

    try:
        stock_data = yf.download(ticker, start=today, end=today)
        if stock_data.empty:
            print("No hay datos hoy.")
            return

        if not os.path.exists(file_path):
            stock_data.to_csv(file_path, mode='w', header=True)
        else:
            existing_data = pd.read_csv(file_path, index_col='Date')
            if today.strftime('%Y-%m-%d') in existing_data.index:
                print("Datos de hoy ya están.")
                return
            stock_data.to_csv(file_path, mode='a', header=False)

        print("Datos guardados exitosamente.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    fetch_and_save_amd_data()
