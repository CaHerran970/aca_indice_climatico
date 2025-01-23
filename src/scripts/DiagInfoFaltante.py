#import xarray as xr
import pandas as pd
import os
import numpy as np
import pdb
#def main():
 #   ruta_datos = "../../data/processed"
  #  file = 'era5_rain_union.nc'
   ##archivo_salida = os.path.join(ruta_datos, "era5_precipitaciones_maximo.nc")

    #periodo_referencia = (1960, 1990)
    #variable = 'tp'  
# Ruta del archivo
file_path = "era5_rain_union.nc"

# Abrir el archivo NetCDF
data = xr.open_dataset(file_path)

# Imprimir la estructura del archivo
print(data)
