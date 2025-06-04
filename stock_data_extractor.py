import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def fetch_and_save_amd_data():
    ticker = "AMD"
    today = datetime.today().date()
    file_path = "amd_stock_data.csv"

    try:
        print("Iniciando descarga de datos...")
        stock_data = yf.download(ticker, start=today, end=today)
        
        if stock_data.empty:
            print("No hay datos disponibles para hoy.")
            return

        # Crear archivo CSV con encabezados si no existe
        if not os.path.exists(file_path):
            print(f"Creando archivo {file_path}...")
            with open(file_path, 'w') as f:
                f.write("Date,Open,High,Low,Close,Adj Close,Volume\n")  # Encabezados

        # Verificar si la fecha ya existe
        existing_data = pd.read_csv(file_path)
        if today.strftime('%Y-%m-%d') in existing_data['Date'].values:
            print("Datos de hoy ya están registrados.")
            return

        # Agregar nuevos datos
        with open(file_path, 'a') as f:
            line = f"{today},{stock_data['Open'][0]},{stock_data['High'][0]},{stock_data['Low'][0]},{stock_data['Close'][0]},{stock_data['Adj Close'][0]},{stock_data['Volume'][0]}\n"
            f.write(line)
            
        print("Datos guardados exitosamente.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    fetch_and_save_amd_data()
