#Este código en Python utiliza las bibliotecas requests, json, pandas, folium y numpy para obtener datos sobre terremotos 
#en los Estados Unidos, convertirlos en un objeto de marco de datos de Pandas y mostrarlos en un mapa utilizando Folium

import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import json  # importa la biblioteca json que se usa para trabajar con datos JSON.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
import numpy as np  # importa la biblioteca numpy como np, que se utiliza para realizar operaciones matemáticas en matrices y arreglos de datos.
from datetime import datetime, timedelta
import sys
# form display import display

url = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"

# filename = 'USA_data.json'
filename = 'USA_data.csv'

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



def sismo_usa_json_etl(url, filename, format):
    
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
    
    # Transformar las columnas de tiempo
    df_sismo["properties.time"] = pd.to_datetime(df_sismo["properties.time"], unit="ms")
    df_sismo["properties.updated"] = pd.to_datetime(df_sismo["properties.updated"], unit="ms")
    
    # Dividir la columna geometry.coordinates en columnas separadas
    df_sismo[["Longitud", "Latitud", "Profundidad"]] = pd.DataFrame(df_sismo["geometry.coordinates"].tolist())
    
    df_sismo.drop(columns=[])
    
    df_sismo.drop(columns=['type',"properties.tz",'properties.tz', 'properties.code','properties.url',
                           'properties.detail','properties.alert', 'properties.status','properties.types','properties.sources','properties.magType',
                           'properties.type', 'properties.title', 'geometry.type'], axis=1, inplace=True)
    # Renombrar las columnas
    df_sismo = df_sismo.rename(columns={"properties.mag": "Magnitud",
                                        "properties.time": "Primer Registro",
                                        "properties.updated": "Último Registro",
                                        "properties.place": "Ubicación",
                                        "Longitud": "Longitud (grados)",
                                        "Latitud": "Latitud (grados)",
                                        "Profundidad": "Profundidad (km)"})
    
    # Guardar el DataFrame en un archivo JSON
    # df_sismo.to_json(path_or_buf= '../DASHBOARD/CSV_ORIGINAL' + filename, orient="records")
    
    # Devolver el DataFrame
    return df_sismo.to_csv(path_or_buf= '../DASHBOARD/CSV_ORIGINAL' + filename, index=False)

sismo_usa_json(url, filename)
if __name__ == '__main__':
    url = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"

# filename = 'USA_data.json'
    filename = 'USA_data.csv'
    sismo_usa_json(url, filename)
