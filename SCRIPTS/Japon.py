#Este código en Python utiliza la biblioteca requests y pandas para recuperar datos sobre terremotos en Japón desde una URL 
# y convertirlos en un objeto de marco de datos de Pandas.

import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import json  # importa la biblioteca json que se usa para trabajar con datos JSON.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
import numpy as np  # importa la biblioteca numpy como np, que se utiliza para realizar operaciones matemáticas en matrices y arreglos de datos.
from datetime import datetime, timedelta
import os
import sys

url= 'https://www.jma.go.jp/bosai/quake/data/list.json'

folder_path_CSV = "../DASHBOARD/CSV_TRANSFORMADOS"
file_name_CSV_CE   = "Datos_japon_0.csv"

folder_path_json_CE = "../JSON/CON_ETL"
file_name_json   = "japan_data_0.json"


url_USGS = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"

filename_json           = 'Japon_data.json'
folder_path_SE_JSON     = '../JSON/SIN_ETL'
folder_path_CE_JSON     = '../JSON/CON_ETL'

filename_csv            = 'Japon_data.csv'
folder_path_SE_CSV      = '../DASHBOARD/CSV_ORIGINAL'
folder_path_CE_CSV      = '../DASHBOARD/CSV_TRANSFORMADOS'



def get_japan_CSV(url, folder_path_CSV,file_name_CSV_CE):
    try:
        response = requests.get(url)
        data = response.json()
        df_japon = pd.DataFrame(data)

        # Transformaciones en el DataFrame
        df_japon['rdt'] = pd.to_datetime(df_japon['rdt'])
        
        df_japon['rdt'] = df_japon['rdt'].dt.tz_localize(None)
        
        df_japon['rdt'] = df_japon['rdt'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        df_japon['at'] = pd.to_datetime(df_japon['at'])
        
        df_japon['at'] = df_japon['at'].dt.tz_localize(None)
        
        df_japon['at'] = df_japon['at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        df_japon.drop(columns=['ctt','ift', 'eid', 'ser','ttl', 'at', 'anm', 'acd','json','int', 'en_ttl', 'en_anm'], inplace=True)
        
        df_japon = df_japon.rename(columns={"rdt": "time",
                                    "eid": "id",
                                    "maxi": "intensidad_max",
                                    "en_ttl": "title",
                                    "en_anm": "nombre_area_epicentral"})        
        
        df_japon['cod'] = df_japon['cod'].str.replace('/$', '')        
        df_japon[['latitud', 'longitud', 'profundidad']] = df_japon['cod'].str.extract(r'([\+\-]\d+\.\d+)([\+\-]\d+\.\d+)([\+\-]\d+)')            
        df_japon.drop(columns='cod', inplace=True)        
        df_japon.dropna(inplace=True)        
        df_japon[['latitud', 'longitud', 'profundidad']] = df_japon[['latitud', 'longitud', 'profundidad']].applymap(lambda x: x[1:] if isinstance(x, str) else x)        
        df_japon[['latitud', 'longitud']] = df_japon[['latitud', 'longitud']].astype(float)        
        df_japon['profundidad'] = df_japon['profundidad'].astype(int)
        
        df_japon['mag'] = df_japon['mag'].astype(float)
        
        df_japon['intensidad_max'].replace('',0,inplace=True)        
        diccionario_valores = {'1': '1', '2': '2', '3': '3', '4': '4', '5-': '5', '5+': '5', '6+': '6'}        
        df_japon['intensidad_max'] = df_japon['intensidad_max'].replace(diccionario_valores)
        df_japon['intensidad_max'] = df_japon['intensidad_max'].fillna(0).astype(int)
        
        df_japon['profundidad'] = df_japon['profundidad'] // 1000
        
        file_path = os.path.join(folder_path_CSV, file_name_CSV_CE)
        
        df_japon.to_csv(file_path, index=False)
        
        return df_japon
        
    except requests.exceptions.RequestException as e:
        print('Error al obtener los datos:', e)
        return None


def get_japan_JSON(url,folder_path_json_CE,file_name_json):
    try:
        # Hacer una solicitud HTTP a la URL definida y convertir la respuesta en un objeto JSON de Python
        response = requests.get(url)
        data = response.json()

        # Convertir el objeto JSON en un marco de datos de Pandas
        df_japan = pd.DataFrame(data)

        # Limpieza de datos
        df_japan['rdt'] = pd.to_datetime(df_japan['rdt']).dt.tz_localize(None).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        df_japan['at'] = pd.to_datetime(df_japan['at']).dt.tz_localize(None).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        df_japan.drop(columns=['ctt','ift', 'eid', 'ser','ttl', 'at', 'anm', 'acd','json','int', 'en_ttl', 'en_anm'], inplace=True)
        
        df_japan = df_japan.rename(columns={"rdt" : "time",
                                            "eid" : "id",
                                            "maxi" : "intensidad_max",
                                            "en_ttl" : "title",
                                            "en_anm" : "nombre_area_epicentral"})
        
        df_japan['cod'] = df_japan['cod'].str.replace('/$', '')
        df_japan[['latitud', 'longitud', 'profundidad']] = df_japan['cod'].str.extract(r'([\+\-]\d+\.\d+)([\+\-]\d+\.\d+)([\+\-]\d+)')
        df_japan.drop(columns='cod', inplace=True)
        df_japan.dropna(inplace=True)
        
        df_japan[['latitud', 'longitud', 'profundidad']] = df_japan[['latitud', 'longitud', 'profundidad']].applymap(lambda x: x[1:] if isinstance(x, str) else x)
        df_japan[['latitud', 'longitud']] = df_japan[['latitud', 'longitud']].astype(float)
        df_japan['profundidad'] = df_japan['profundidad'].astype(int)
        df_japan['mag'] = df_japan['mag'].astype(float)
        df_japan['intensidad_max'].replace('',0,inplace=True)
        diccionario_valores = {'1': '1', '2': '2', '3': '3', '4': '4', '5-': '5', '5+': '5', '6+': '6'}
        df_japan['intensidad_max'] = df_japan['intensidad_max'].replace(diccionario_valores)
        df_japan['intensidad_max'] = df_japan['intensidad_max'].fillna(0).astype(int)
        df_japan['profundidad'] = df_japan['profundidad'] // 1000

        # Guardar el resultado en un archivo JSON
        
        file_path = os.path.join(folder_path_json_CE, file_name_json)
        
        
        df_japan.to_json(file_path, orient='records')

        # Devolver el marco de datos resultante
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud HTTP: {e}")
    except ValueError as e:
        print(f"Error al decodificar el objeto JSON: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")
        
        
        
        

def sismo_japon_json(url_USGS,filename_json,folder_path_SE_JSON):
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99, "limit": 20000}
    
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


def sismo_japon_json_etl(url_USGS, filename_json,folder_path_CE_JSON):
    
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99, "limit": 20000}
    
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



def sismo_japon_CSV(url_USGS,folder_path_SE_CSV, filename_csv):
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99, "limit": 20000}
    
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



def sismo_japon_CSV_ETL(url_USGS, filename_csv,folder_path_CE_CSV):
    
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99, "limit": 20000}
    
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
    
    file_path = os.path.join(folder_path_CE_CSV, filename_csv)
    df_sismo.to_csv(file_path, index=False)
    
    # Devolver el DataFrame
    return df_sismo
