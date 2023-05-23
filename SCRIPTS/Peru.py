
import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import json  # importa la biblioteca json que se usa para trabajar con datos JSON.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
import numpy as np  # importa la biblioteca numpy como np, que se utiliza para realizar operaciones matemáticas en matrices y arreglos de datos.
from datetime import datetime, timedelta
import os
import sys

url_USGS = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"

filename_json           = 'Peru_data.json'
folder_path_SE_JSON     = '../JSON/SIN_ETL'
folder_path_CE_JSON     = '../JSON/CON_ETL'

filename_csv            = 'Peru_data.csv'
folder_path_SE_CSV      = '../DASHBOARD/CSV_ORIGINAL'
folder_path_CE_CSV      = '../DASHBOARD/CSV_TRANSFORMADOS'



def sismo_Peru_json(url_USGS,filename_json,folder_path_SE_JSON):
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": -18.521, "maxlatitude": 0.132, "minlongitude": -84.419, "maxlongitude": -68.599, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url_USGS, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    # Guardar el resultado en un archivo JSON        
    file_path = os.path.join(folder_path_SE_JSON, filename_json)
    df_sismo.to_json(file_path, orient='records')
    
    return df_sismo


def sismo_Peru_json_etl(url_USGS, filename_json,folder_path_CE_JSON):
    
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": -18.521, "maxlatitude": 0.132, "minlongitude": -84.419, "maxlongitude": -68.599, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url_USGS, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    df_sismo.drop(columns=['type','properties.alert','properties.tz','properties.code',
                           'properties.url','properties.detail','properties.net',
                           'properties.status','properties.types','properties.sources',
                           'properties.magType','properties.type','geometry.type','properties.title'], axis=1, inplace=True)
    
    df_sismo['Pais'] = df_sismo['properties.place'].str.split(',').str[1].str.strip()
    df_sismo['properties.place'] = df_sismo['properties.place'].str.split(',', expand=True)[0]
    
    # Transformar las columnas de tiempo
    df_sismo["properties.time"] = pd.to_datetime(df_sismo["properties.time"], unit="ms")
    df_sismo["properties.updated"] = pd.to_datetime(df_sismo["properties.updated"], unit="ms")
            
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
        
    df_sismo["Longitud"] = df_sismo["Longitud"].astype(float) 
    df_sismo["Latitud"] = df_sismo["Latitud"].astype(float) 
    df_sismo["Profundidad"] = df_sismo["Profundidad"].astype(float)   
    
    file_path = os.path.join(folder_path_CE_JSON, filename_json)
    df_sismo.to_json(file_path, orient='records')
    
    # Devolver el DataFrame
    return df_sismo



def sismo_Peru_CSV(url_USGS,folder_path_SE_CSV, filename_csv):
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": -18.521, "maxlatitude": 0.132, "minlongitude": -84.419, "maxlongitude": -68.599, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url_USGS, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    # Guardar el resultado en un archivo JSON        
    file_path = os.path.join(folder_path_SE_CSV, filename_csv)
    df_sismo.to_csv(file_path, index=False)
    
    return df_sismo



def sismo_Peru_CSV_ETL(url_USGS, filename_csv,folder_path_CE_CSV):
    
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": -18.521, "maxlatitude": 0.132, "minlongitude": -84.419, "maxlongitude": -68.599, "limit": 20000}
    
    # Realizar la solicitud a la API de USGS
    response = requests.get(url_USGS, params=params)
    data = response.json()
    
    # Obtener solo las características (features)
    features = data['features']
    
    # Convertir las características a un DataFrame
    df_sismo = pd.json_normalize(features)
    
    df_sismo.drop(columns=['type','properties.alert','properties.tz','properties.code','properties.url','properties.detail','properties.net'
                       ,'properties.status','properties.types','properties.sources','properties.magType','properties.type','geometry.type',
                       'properties.title'], axis=1, inplace=True)
    
    df_sismo['Pais'] = df_sismo['properties.place'].str.split(',').str[1].str.strip()
    df_sismo['properties.place'] = df_sismo['properties.place'].str.split(',', expand=True)[0]
    
    # Transformar las columnas de tiempo
    df_sismo["properties.time"] = pd.to_datetime(df_sismo["properties.time"], unit="ms")
    df_sismo["properties.updated"] = pd.to_datetime(df_sismo["properties.updated"], unit="ms")
    
        
    # Dividir la columna geometry.coordinates en columnas separadas
    df_sismo[["Longitud", "Latitud", "Profundidad"]] = pd.DataFrame(df_sismo["geometry.coordinates"].tolist())
    
    df_sismo.drop("geometry.coordinates", axis=1, inplace=True) 
       
    df_sismo = df_sismo.rename(columns={'properties.mag':      'Magnitud',   
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
     
    df_sismo["Longitud"] = df_sismo["Longitud"].astype(float) 
    df_sismo["Latitud"] = df_sismo["Latitud"].astype(float) 
    df_sismo["Profundidad"] = df_sismo["Profundidad"].astype(float)   
    
    file_path = os.path.join(folder_path_CE_CSV, filename_csv)
    df_sismo.to_csv(file_path, index=False)

    
    # Devolver el DataFrame
    return df_sismo
