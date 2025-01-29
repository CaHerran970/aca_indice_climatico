import xarray as xr
import os
import matplotlib.pyplot as plt
import pandas as pd

# Ruta actualizada del archivo NetCDF
file_path = "C:/Users/1019041572/Documents/Github/aca_indice_climatico/data/raw/era5_rain_union.nc"

# Abrir el archivo NetCDF
data = xr.open_dataset(file_path)

# Imprimir la estructura del archivo
print(data)

# Listar variables disponibles
print("\nVariables disponibles en el archivo:")
print(data.variables)
# Ver los primeros valores de la variable 'tp'
print(data['tp'])

# Ver estadísticas básicas de la variable 'tp'
print(data['tp'].mean())  # Promedio de precipitación
print(data['tp'].max())   # Máximo valor
print(data['tp'].min())   # Mínimo valor

# Seleccionar la primera capa temporal de la variable 'tp'
rain_data = data["tp"].isel(time=0)

# Graficar
#plt.figure(figsize=(10, 6))
#rain_data.plot()
#plt.title("Mapa de precipitación (primer tiempo)")
#plt.show()

# Seleccionar la variable de interés (ejemplo: 'tp' para precipitación)
df = data["tp"].to_dataframe().reset_index()

# Mostrar los primeros 100 registros
print(df.head(1000))

# Guardar los primeros 100 registros en un CSV
df.head(1000).to_csv("primeros_100_registros.csv", index=False)

print("Archivo guardado como 'primeros_100_registros.csv'. Ábrelo en VS Code para verlo como tabla.")