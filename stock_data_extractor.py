#!/usr/bin/env python3
"""
Stock Data Extractor - AMD
Extrae datos diarios del stock de AMD y los guarda en CSV
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

def main():
    """Función principal para extraer datos de AMD"""
    
    print("=" * 50)
    print("Stock Data Extractor - AMD")
    print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        # Configuración
        ticker_symbol = "AMD"
        output_file = "amd_stock_data.csv"  # Nombre que espera el workflow
        
        # Crear objeto ticker
        print(f"\n📊 Descargando datos de {ticker_symbol}...")
        ticker = yf.Ticker(ticker_symbol)
        
        # Obtener datos históricos (últimos 30 días para tener suficiente información)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Descargar datos
        historical_data = ticker.history(start=start_date, end=end_date)
        
        if historical_data.empty:
            print("❌ No se pudieron obtener datos históricos")
            sys.exit(1)
        
        # Obtener información adicional del ticker
        info = ticker.info
        
        # Preparar DataFrame con datos relevantes
        df = historical_data.copy()
        df['Symbol'] = ticker_symbol
        
        # Agregar columnas adicionales si están disponibles
        if info:
            df['MarketCap'] = info.get('marketCap', None)
            df['PERatio'] = info.get('trailingPE', None)
            df['Beta'] = info.get('beta', None)
        
        # Resetear índice para que Date sea una columna
        df.reset_index(inplace=True)
        
        # Formatear fecha
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # Reorganizar columnas
        columns_order = ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
        if 'MarketCap' in df.columns:
            columns_order.extend(['MarketCap', 'PERatio', 'Beta'])
        
        df = df[columns_order]
        
        # Guardar en CSV
        df.to_csv(output_file, index=False)
        print(f"\n✅ Datos guardados exitosamente en '{output_file}'")
        
        # Mostrar resumen del último día
        latest_data = df.iloc[-1]
        print(f"\n📈 Resumen del último día de trading ({latest_data['Date']}):")
        print(f"   Apertura:  ${latest_data['Open']:.2f}")
        print(f"   Máximo:    ${latest_data['High']:.2f}")
        print(f"   Mínimo:    ${latest_data['Low']:.2f}")
        print(f"   Cierre:    ${latest_data['Close']:.2f}")
        print(f"   Volumen:   {int(latest_data['Volume']):,}")
        
        # Calcular cambio porcentual
        if len(df) > 1:
            previous_close = df.iloc[-2]['Close']
            change = latest_data['Close'] - previous_close
            change_percent = (change / previous_close) * 100
            print(f"   Cambio:    ${change:.2f} ({change_percent:+.2f}%)")
        
        # Información adicional si está disponible
        if info:
            print(f"\n📊 Información adicional de {ticker_symbol}:")
            print(f"   Nombre:           {info.get('longName', 'N/A')}")
            print(f"   Sector:           {info.get('sector', 'N/A')}")
            print(f"   Industria:        {info.get('industry', 'N/A')}")
            print(f"   Capitalización:   ${info.get('marketCap', 0):,.0f}")
            print(f"   P/E Ratio:        {info.get('trailingPE', 'N/A')}")
            print(f"   Beta:             {info.get('beta', 'N/A')}")
            print(f"   52 semanas alto:  ${info.get('fiftyTwoWeekHigh', 'N/A')}")
            print(f"   52 semanas bajo:  ${info.get('fiftyTwoWeekLow', 'N/A')}")
        
        print("\n✅ Extracción completada exitosamente")
        
        # Verificar que el archivo se creó correctamente
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"📁 Archivo creado: {output_file} ({file_size} bytes)")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error durante la extracción: {str(e)}")
        
        # Crear archivo vacío para evitar que falle el workflow
        try:
            # Crear un CSV mínimo con datos de prueba
            emergency_data = pd.DataFrame([{
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Symbol': 'AMD',
                'Open': 0.0,
                'High': 0.0,
                'Low': 0.0,
                'Close': 0.0,
                'Volume': 0,
                'Error': str(e)
            }])
            emergency_data.to_csv(output_file, index=False)
            print(f"⚠️  Archivo de emergencia creado: {output_file}")
        except:
            print("❌ No se pudo crear archivo de emergencia")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
