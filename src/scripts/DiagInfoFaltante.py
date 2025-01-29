import xarray as xr
import pandas as pd
import numpy as np

# Ruta del archivo
file_path = "C:/Users/1019041572/Documents/Github/aca_indice_climatico/data/raw/era5_rain_union.nc"

# Cargar el archivo NetCDF
data = xr.open_dataset(file_path)

# Seleccionar la variable de precipitación ('tp')
df = data["tp"].to_dataframe().reset_index()

# Identificar valores NaN
df["is_nan"] = df["tp"].isna()

# Contar datos faltantes por día
missing_by_day = df.groupby("time")["is_nan"].sum()

# Contar datos faltantes por mes
df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
missing_by_month = df.groupby(["year", "month"])["is_nan"].sum()

#  Contar datos faltantes por año
missing_by_year = df.groupby("year")["is_nan"].sum()

#  Contar datos faltantes por coordenada
missing_by_coord = df.groupby(["year", "month","latitude", "longitude"])["is_nan"].sum()

# Función para detectar períodos consecutivos sin datos
def detect_missing_periods(series, label):
    periods = []
    count = 0
    start = None
    for date, missing in series.items():
        if missing > 0:  # Si hay valores NaN
            if start is None:
                start = date
            count += 1
        else:
            if count > 0:
                periods.append((start, date, count))
                count = 0
                start = None
    if count > 0:
        periods.append((start, date, count))
    
    return pd.DataFrame(periods, columns=[f"{label}_start", f"{label}_end", f"{label}_missing_days"])

#  Detectar períodos consecutivos sin datos
missing_periods_daily = detect_missing_periods(missing_by_day, "daily")
missing_periods_monthly = detect_missing_periods(missing_by_month, "monthly")
missing_periods_yearly = detect_missing_periods(missing_by_year, "yearly")

# Guardar resultados en archivos CSV
missing_by_day.to_csv("missing_by_day.csv")
missing_by_month.to_csv("missing_by_month.csv")
missing_by_year.to_csv("missing_by_year.csv")
missing_by_coord.to_csv("missing_by_coord.csv")
missing_periods_daily.to_csv("missing_periods_daily.csv", index=False)
missing_periods_monthly.to_csv("missing_periods_monthly.csv", index=False)
missing_periods_yearly.to_csv("missing_periods_yearly.csv", index=False)

#  Mostrar resultados en consola
print(" Diagnóstico de datos faltantes:")
print("Total de datos faltantes: {df['is_nan'].sum()}")
print(" Datos faltantes por año:")
print(missing_by_year)
print("Datos faltantes por coordenada:")
print(missing_by_coord)
print("Períodos consecutivos sin datos (diarios):")
print(missing_periods_daily.head(10))  # Muestra solo los primeros 10 períodos
