#Este código en Python utiliza las bibliotecas requests, json, pandas, folium y numpy para obtener datos sobre terremotos 
#en los Estados Unidos, convertirlos en un objeto de marco de datos de Pandas y mostrarlos en un mapa utilizando Folium

import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import json  # importa la biblioteca json que se usa para trabajar con datos JSON.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
import numpy as np  # importa la biblioteca numpy como np, que se utiliza para realizar operaciones matemáticas en matrices y arreglos de datos.
from datetime import datetime, timedelta

url = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"

filename = 'USA_data.json'

def sismo_usa_json(url):
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
    
    return df_sismo



def sismo_usa_json(url, filename):
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
    
    # Guardar el DataFrame en un archivo JSON
    df_sismo.to_json(path_or_buf= '../JSON/CON_ETL/' +filename, orient="records")
    
    # Devolver el DataFrame
    return df_sismo
