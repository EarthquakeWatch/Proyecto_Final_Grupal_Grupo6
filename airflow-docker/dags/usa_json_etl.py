import requests
import pandas as pd  
from datetime import datetime, timedelta
# import sys
import os

def sismo_usa_json_etl(url, filename):
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.6, "maxlatitude": 50, "minlongitude": -125, "maxlongitude": -65, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    # Seleccionar las columnas necesarias
    df_sismo = df_sismo[["properties.mag", "properties.time", "properties.updated", "properties.tz",
                         "properties.place", "properties.type", "geometry.coordinates"]]
    
    # Transformar las columnas de tiempo
    df_sismo["properties.time"] = pd.to_datetime(df_sismo["properties.time"], unit="ms")
    df_sismo["properties.updated"] = pd.to_datetime(df_sismo["properties.updated"], unit="ms")
    
    # Dividir la columna geometry.coordinates en columnas separadas
    df_sismo[["Longitud", "Latitud", "Profundidad"]] = pd.DataFrame(df_sismo["geometry.coordinates"].tolist())
    
    # Seleccionar las columnas necesarias
    df_sismo = df_sismo[["properties.mag", "properties.time", "properties.updated", "properties.place",
                         "Longitud", "Latitud", "Profundidad"]]
    
    # Renombrar las columnas
    df_sismo = df_sismo.rename(columns={"properties.mag": "Magnitud",
                                        "properties.time": "Primer Registro",
                                        "properties.updated": "Último Registro",
                                        "properties.place": "Ubicación",
                                        "Longitud": "Longitud (grados)",
                                        "Latitud": "Latitud (grados)",
                                        "Profundidad": "Profundidad (km)"})
    print("Directorio de trabajo actual:", os.getcwd())
    # Guardar el DataFrame en un archivo JSON
    df_sismo.to_json(path_or_buf= '.' + filename, orient="records")
    return os.getcwd() + filename

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python script.py <json>")
#         sys.exit(1)
#     json_file_path = sys.argv[1]