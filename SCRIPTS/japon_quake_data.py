#Este código en Python utiliza la biblioteca requests y pandas para recuperar datos sobre terremotos en Japón desde una URL 
# y convertirlos en un objeto de marco de datos de Pandas.

import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
from datetime import datetime, timedelta

url= 'https://www.jma.go.jp/bosai/quake/data/list.json'  # define la URL de donde se va a extraer los datos.

def get_japan_quake_df(url):
    response = requests.get(url)
    data = response.json()
    df_japan = pd.DataFrame(data)
    return df_japan


def get_japan_quake_data(url):
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
        df_japan = df_japan.rename(columns={"rdt" : "time", "eid" : "id", "maxi" : "intensidad_max", "en_ttl" : "title", "en_anm" : "nombre_area_epicentral"})
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
        df_japan.to_json('../JSON/CON_ETL/japan_data.json', orient='records')

        # Devolver el marco de datos resultante
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud HTTP: {e}")
    except ValueError as e:
        print(f"Error al decodificar el objeto JSON: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")