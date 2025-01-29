import xarray as xr
import pandas as pd
import numpy as np

# Ruta del archivo
file_path = "C:/Users/1019041572/Documents/Github/aca_indice_climatico/data/raw/era5_rain_union.nc"

ds = xr.open_dataset(file_path)

# Seleccionar la variable de precipitación
da_tp = ds['tp']

# Convertir a DataFrame
df = da_tp.to_dataframe().reset_index()

# Convertir la columna 'time' a formato datetime
df['time'] = pd.to_datetime(df['time'])

# Agregar columnas de año y mes
df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month
df['day'] = df['time'].dt.date  # Solo la fecha sin la hora

### 📊 **1. Conteo de valores faltantes (NaN)**
missing_counts = {
    "Total de valores NaN en tp": df['tp'].isna().sum(),
    "Valores NaN por día": df.groupby('day')['tp'].apply(lambda x: x.isna().sum()),
    "Valores NaN por mes": df.groupby(['year', 'month'])['tp'].apply(lambda x: x.isna().sum()),
    "Valores NaN por año": df.groupby('year')['tp'].apply(lambda x: x.isna().sum()),
    "Valores NaN por ubicación (lat, lon)": df.groupby(['latitude', 'longitude'])['tp'].apply(lambda x: x.isna().sum())
}

### 📉 **2. Identificación de períodos consecutivos sin datos**
def consecutive_missing(series):
    """ Encuentra períodos consecutivos de valores NaN """
    is_missing = series.isna()
    groups = (is_missing != is_missing.shift()).cumsum()
    missing_periods = series.groupby(groups).apply(lambda x: len(x) if x.isna().all() else 0)
    return missing_periods[missing_periods > 0]

missing_periods = {
    "Días consecutivos sin datos": consecutive_missing(df.set_index('time')['tp']),
    "Meses consecutivos sin datos": consecutive_missing(df.set_index(['year', 'month'])['tp']),
    "Años consecutivos sin datos": consecutive_missing(df.set_index('year')['tp']),
}

### 📊 **3. Mostrar resumen**
print("🔍 Diagnóstico de datos faltantes:")
for key, value in missing_counts.items():
    print(f"\n➡ {key}:")
    print(value)

print("\n🔄 Períodos consecutivos sin datos:")
for key, value in missing_periods.items():
    print(f"\n➡ {key}:")
    print(value)
