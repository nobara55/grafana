#!/usr/bin/env python3
"""
Script para extraer datos diarios del stock de AMD
Autor: Tu Nombre
Fecha: 2025
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AMDStockExtractor:
    def __init__(self):
        self.ticker = "AMD"
        self.stock = yf.Ticker(self.ticker)
        self.data_dir = "data"
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Crear directorio de datos si no existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Directorio {self.data_dir} creado")
    
    def extract_daily_data(self):
        """Extraer datos del día actual"""
        try:
            # Obtener datos del día
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
            
            # Descargar datos históricos (últimos 5 días para asegurar que tenemos el último día de trading)
            hist_data = self.stock.history(period="5d")
            
            if hist_data.empty:
                logger.warning("No se encontraron datos históricos")
                return None
            
            # Obtener el último día de trading
            last_trading_day = hist_data.index[-1].date()
            last_day_data = hist_data.iloc[-1]
            
            # Crear diccionario con los datos
            daily_data = {
                "date": str(last_trading_day),
                "symbol": self.ticker,
                "open": float(last_day_data['Open']),
                "high": float(last_day_data['High']),
                "low": float(last_day_data['Low']),
                "close": float(last_day_data['Close']),
                "volume": int(last_day_data['Volume']),
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Obtener información adicional
            info = self.stock.info
            daily_data.update({
                "market_cap": info.get('marketCap', None),
                "pe_ratio": info.get('trailingPE', None),
                "dividend_yield": info.get('dividendYield', None),
                "52_week_high": info.get('fiftyTwoWeekHigh', None),
                "52_week_low": info.get('fiftyTwoWeekLow', None),
                "avg_volume": info.get('averageVolume', None),
                "beta": info.get('beta', None)
            })
            
            logger.info(f"Datos extraídos exitosamente para {last_trading_day}")
            return daily_data
            
        except Exception as e:
            logger.error(f"Error al extraer datos: {str(e)}")
            return None
    
    def save_to_json(self, data):
        """Guardar datos en formato JSON"""
        if not data:
            return
        
        filename = f"{self.data_dir}/amd_stock_{data['date']}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        logger.info(f"Datos guardados en {filename}")
    
    def save_to_csv(self, data):
        """Agregar datos a un archivo CSV histórico"""
        if not data:
            return
        
        csv_filename = f"{self.data_dir}/amd_stock_history.csv"
        
        # Convertir a DataFrame
        df_new = pd.DataFrame([data])
        
        # Si el archivo existe, agregar datos
        if os.path.exists(csv_filename):
            df_existing = pd.read_csv(csv_filename)
            # Evitar duplicados
            if data['date'] not in df_existing['date'].values:
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv(csv_filename, index=False)
                logger.info(f"Datos agregados a {csv_filename}")
            else:
                logger.info(f"Los datos para {data['date']} ya existen en el CSV")
        else:
            # Crear nuevo archivo
            df_new.to_csv(csv_filename, index=False)
            logger.info(f"Nuevo archivo CSV creado: {csv_filename}")
    
    def generate_summary_report(self):
        """Generar un reporte resumido"""
        csv_filename = f"{self.data_dir}/amd_stock_history.csv"
        
        if not os.path.exists(csv_filename):
            logger.warning("No hay datos históricos para generar reporte")
            return
        
        df = pd.read_csv(csv_filename)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calcular estadísticas
        latest_close = df.iloc[-1]['close']
        avg_close_30d = df.tail(30)['close'].mean() if len(df) >= 30 else df['close'].mean()
        max_close_30d = df.tail(30)['close'].max() if len(df) >= 30 else df['close'].max()
        min_close_30d = df.tail(30)['close'].min() if len(df) >= 30 else df['close'].min()
        
        report = {
            "report_date": datetime.now().isoformat(),
            "latest_close": latest_close,
            "avg_close_30d": avg_close_30d,
            "max_close_30d": max_close_30d,
            "min_close_30d": min_close_30d,
            "total_records": len(df)
        }
        
        # Guardar reporte
        report_filename = f"{self.data_dir}/amd_stock_report_latest.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=4)
        
        logger.info(f"Reporte generado: {report_filename}")
        return report

def main():
    """Función principal"""
    logger.info("=== Iniciando extracción de datos AMD ===")
    
    extractor = AMDStockExtractor()
    
    # Extraer datos del día
    daily_data = extractor.extract_daily_data()
    
    if daily_data:
        # Guardar en JSON
        extractor.save_to_json(daily_data)
        
        # Guardar en CSV
        extractor.save_to_csv(daily_data)
        
        # Generar reporte
        report = extractor.generate_summary_report()
        
        logger.info("=== Extracción completada exitosamente ===")
        
        # Imprimir resumen
        print(f"\nResumen del día {daily_data['date']}:")
        print(f"Apertura: ${daily_data['open']:.2f}")
        print(f"Cierre: ${daily_data['close']:.2f}")
        print(f"Máximo: ${daily_data['high']:.2f}")
        print(f"Mínimo: ${daily_data['low']:.2f}")
        print(f"Volumen: {daily_data['volume']:,}")
        
        if report:
            print(f"\nEstadísticas (últimos 30 días):")
            print(f"Promedio de cierre: ${report['avg_close_30d']:.2f}")
            print(f"Máximo: ${report['max_close_30d']:.2f}")
            print(f"Mínimo: ${report['min_close_30d']:.2f}")
    else:
        logger.error("No se pudieron extraer datos")

if __name__ == "__main__":
    main()
