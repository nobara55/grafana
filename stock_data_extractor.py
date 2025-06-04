#!/usr/bin/env python3
import yfinance as yf
import sys

print("=== AMD Stock Data Extractor ===")

try:
    # Descargar datos de AMD
    print("Descargando datos de AMD...")
    data = yf.download("AMD", period="5d", progress=False)
    
    if data.empty:
        print("Error: No se obtuvieron datos")
        sys.exit(1)
    
    # Guardar en CSV
    output_file = "amd_stock_data.csv"
    data.to_csv(output_file)
    
    # Mostrar información
    print(f"✅ Archivo guardado: {output_file}")
    print(f"📊 Registros: {len(data)}")
    print(f"💰 Último precio: ${data['Close'].iloc[-1]:.2f}")
    print(f"📅 Última fecha: {data.index[-1].strftime('%Y-%m-%d')}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    
    # Crear archivo vacío para evitar que falle el workflow
    with open("amd_stock_data.csv", "w") as f:
        f.write("Date,Open,High,Low,Close,Volume\n")
        f.write("2025-01-01,0,0,0,0,0\n")
    
    print("⚠️ Archivo de respaldo creado")
    sys.exit(1)

print("✅ Proceso completado")
