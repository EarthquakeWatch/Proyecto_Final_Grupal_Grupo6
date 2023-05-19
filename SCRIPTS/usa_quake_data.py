#Este código en Python utiliza las bibliotecas requests, json, pandas, folium y numpy para obtener datos sobre terremotos 
#en los Estados Unidos, convertirlos en un objeto de marco de datos de Pandas y mostrarlos en un mapa utilizando Folium

import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import json  # importa la biblioteca json que se usa para trabajar con datos JSON.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
import numpy as np  # importa la biblioteca numpy como np, que se utiliza para realizar operaciones matemáticas en matrices y arreglos de datos.
from datetime import datetime, timedelta
import os
import sys
# form display import display

url = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"

filename_json           = 'USA_data.json'
folder_path_SE_JSON     = '../JSON/SIN_ETL'
folder_path_CE_JSON     = '../JSON/CON_ETL'

filename_csv            = 'USA_data.csv'
folder_path_SE_CSV      = '../DASHBOARD/CSV_ORIGINAL'
folder_path_CE_CSV      = '../DASHBOARD/CSV_TRANSFORMADOS'

def sismo_usa_json(url,filename_json,folder_path_SE_JSON):
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    # Guardar el resultado en un archivo JSON        
    file_path = os.path.join(folder_path_SE_JSON, filename_json)
    df_sismo.to_json(file_path, orient='records')
    
    return df_sismo


def sismo_usa_json_etl(url, filename_json,folder_path_CE_JSON):
    
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    df_sismo.drop(columns=['type','properties.alert','properties.tz','properties.code',
                           'properties.url','properties.detail','properties.net',
                           'properties.status','properties.types','properties.sources',
                           'properties.magType','properties.type','geometry.type','properties.title'], axis=1, inplace=True)
    
    # Transformar las columnas de tiempo
    df_sismo["properties.time"] = pd.to_datetime(df_sismo["properties.time"], unit="ms")
    df_sismo["properties.updated"] = pd.to_datetime(df_sismo["properties.updated"], unit="ms")
    
    df_sismo['estado'] = df_sismo['properties.place'].str.split(',').str[1].str.strip()
    df_sismo['properties.place'] = df_sismo['properties.place'].str.split(',', expand=True)[0]
        
    # Dividir la columna geometry.coordinates en columnas separadas
    df_sismo[["Longitud", "Latitud", "Profundidad"]] = pd.DataFrame(df_sismo["geometry.coordinates"].tolist())
    
    df_sismo.drop("geometry.coordinates", axis=1, inplace=True) 
       
    df_sismo = df_sismo.rename(columns={'properties.mag':      'Magnituud',
                                        'properties.place':    'Place',
                                        'properties.time':     'Fecha',
                                        'properties.updated':  'Ultimo registro',
                                        'properties.felt':     'Felt',
                                        'properties.cdi':      'cdi',
                                        'properties.mmi':      'mmi',
                                        'properties.tsunami':  'Posibilidad tsunami',
                                        'properties.sig':      'Importancia del evento',
                                        'properties.ids':      'Ids',
                                        'properties.nst':      'nst',
                                        'properties.dmin':     'Distancia Horizontal Epicentro',
                                        'properties.rms':      'RMS',
                                        'properties.gap':      'Brecha Azimutal'})
     
    df_sismo['estado'] = df_sismo['estado'].replace({'United States': "Sin Dato",
                                                     'Sandywoods Township': "Sin Dato",
                                                     "CA":"California",
                                                     "WA": "Washington",
                                                     "WY": "Wyoming",
                                                     "UT": "Utah",
                                                     "TN": "Tennessee",
                                                     "TX": "Texas",
                                                     "ID": "Idaho",
                                                     "KS": "Kansas",
                                                     "MO": "Misuri",
                                                     "MT": "Montana",
                                                     "NM": "Nuevo Mexico",
                                                     "Mexico": "New Mexico",
                                                     "NV": "Nevada",
                                                     "NV Earthquake":"Nevada",
                                                     "OK": "Oklahoma",
                                                     'MN': "Minnesota",
                                                     'CO': 'Colorado',
                                                     'AZ': 'Arizona',
                                                     'OR': 'Oregon',
                                                     'Son.': 'Sonora',
                                                     'CA Earthquake': 'California',
                                                     'California Earthquake': "California",
                                                     'NE':"Nebraska"})
    
    df_sismo["Longitud"] = df_sismo["Longitud"].astype(float) 
    df_sismo["Latitud"] = df_sismo["Latitud"].astype(float) 
    df_sismo["Profundidad"] = df_sismo["Profundidad"].astype(float)   
    
    file_path = os.path.join(folder_path_CE_JSON, filename_json)
    df_sismo.to_json(file_path, orient='records')
    
    # Devolver el DataFrame
    return df_sismo



def sismo_usa_CSV(url,folder_path_SE_CSV, filename_csv):
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    # Guardar el resultado en un archivo JSON        
    file_path = os.path.join(folder_path_SE_CSV, filename_csv)
    df_sismo.to_csv(file_path, index=False)
    
    return df_sismo



def sismo_usa_CSV_ETL(url, filename_csv,folder_path_CE_CSV):
    
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    df_sismo.drop(columns=['type','properties.alert','properties.tz','properties.code','properties.url','properties.detail','properties.net'
                       ,'properties.status','properties.types','properties.sources','properties.magType','properties.type','geometry.type',
                       'properties.title'], axis=1, inplace=True)
    
    # Transformar las columnas de tiempo
    df_sismo["properties.time"] = pd.to_datetime(df_sismo["properties.time"], unit="ms")
    df_sismo["properties.updated"] = pd.to_datetime(df_sismo["properties.updated"], unit="ms")
    
    df_sismo['estado'] = df_sismo['properties.place'].str.split(',').str[1].str.strip()
    df_sismo['properties.place'] = df_sismo['properties.place'].str.split(',', expand=True)[0]
        
    # Dividir la columna geometry.coordinates en columnas separadas
    df_sismo[["Longitud", "Latitud", "Profundidad"]] = pd.DataFrame(df_sismo["geometry.coordinates"].tolist())
    
    df_sismo.drop("geometry.coordinates", axis=1, inplace=True) 
       
    df_sismo = df_sismo.rename(columns={'properties.mag':      'Magnituud',   
                                        'properties.place':    'Place',
                                        'properties.time':     'Fecha',  
                                        'properties.updated':  'Ultimo registro', 
                                        'properties.felt':     'Felt',
                                        'properties.cdi':      'cdi',
                                        'properties.mmi':      'mmi', 
                                        'properties.tsunami':  'Posibilidad tsunami',
                                        'properties.sig':      'Importancia del evento',
                                        'properties.ids':      'Ids',
                                        'properties.nst':      'nst',
                                        'properties.dmin':     'Distancia Horizontal Epicentro',
                                        'properties.rms':      'RMS',
                                        'properties.gap':      'Brecha Azimutal'})
     
    df_sismo['estado'] = df_sismo['estado'].replace({'United States': "Sin Dato",
                                                     'Sandywoods Township': "Sin Dato",
                                                     "CA":"California",
                                                     "WA": "Washington",
                                                     "WY": "Wyoming",
                                                     "UT": "Utah",
                                                     "TN": "Tennessee",
                                                     "TX": "Texas",
                                                     "ID": "Idaho",
                                                     "KS": "Kansas",
                                                     "MO": "Misuri",
                                                     "MT": "Montana",
                                                     "NM": "Nuevo Mexico",
                                                     "Mexico": "New Mexico",
                                                     "NV": "Nevada",
                                                     "NV Earthquake":"Nevada",
                                                     "OK": "Oklahoma",
                                                     'MN': "Minnesota",
                                                     'CO': 'Colorado',
                                                     'AZ': 'Arizona',
                                                     'OR': 'Oregon',
                                                     'Son.': 'Sonora',
                                                     'CA Earthquake': 'California',
                                                     'California Earthquake': "California",
                                                     'NE':"Nebraska"})
    
    df_sismo["Longitud"] = df_sismo["Longitud"].astype(float) 
    df_sismo["Latitud"] = df_sismo["Latitud"].astype(float) 
    df_sismo["Profundidad"] = df_sismo["Profundidad"].astype(float)   
    
    file_path = os.path.join(folder_path_CE_CSV, filename_csv)
    df_sismo.to_csv(file_path, index=False)
    
    # Devolver el DataFrame
    return df_sismo