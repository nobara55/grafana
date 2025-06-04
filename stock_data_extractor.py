#!/usr/bin/env python3
"""
Script simplificado para extraer datos de AMD
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def main():
    print("=== Iniciando extracción de datos AMD ===")
    
    # Crear directorio data si no existe
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Directorio 'data' creado")
    
    try:
        # Descargar datos de AMD
        print("Descargando datos de AMD...")
        amd = yf.Ticker("AMD")
        
        # Obtener datos históricos (últimos 5 días)
        hist = amd.history(period="5d")
        
        if hist.empty:
            print("No se encontraron datos")
            return
        
        # Obtener último día de trading
        last_date = hist.index[-1]
        last_data = hist.iloc[-1]
        
        print(f"Último día de trading: {last_date.date()}")
        print(f"Precio de cierre: ${last_data['Close']:.2f}")
        
        # Preparar datos para guardar
        new_row = {
            'Date': last_date.strftime('%Y-%m-%d'),
            'Open': last_data['Open'],
            'High': last_data['High'],
            'Low': last_data['Low'],
            'Close': last_data['Close'],
            'Volume': last_data['Volume']
        }
        
        # Archivo CSV
        csv_file = 'data/amd_stock_history.csv'
        
        # Leer datos existentes o crear nuevo DataFrame
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            # Verificar si el día ya existe
            if new_row['Date'] not in df['Date'].values:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(csv_file, index=False)
                print(f"Datos agregados a {csv_file}")
            else:
                print(f"Los datos para {new_row['Date']} ya existen")
        else:
            df = pd.DataFrame([new_row])
            df.to_csv(csv_file, index=False)
            print(f"Archivo creado: {csv_file}")
        
        # También guardar un archivo JSON con el último día
        import json
        json_file = f"data/amd_latest.json"
        with open(json_file, 'w') as f:
            json.dump(new_row, f, indent=4, default=str)
        print(f"Datos guardados en {json_file}")
        
        print("=== Extracción completada ===")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Crear archivo de prueba para verificar que el workflow funciona
        test_file = 'data/test_file.txt'
        with open(test_file, 'w') as f:
            f.write(f"Test ejecutado el {datetime.now()}\n")
            f.write(f"Error encontrado: {str(e)}\n")
        print(f"Archivo de prueba creado: {test_file}")

if __name__ == "__main__":
    main()
