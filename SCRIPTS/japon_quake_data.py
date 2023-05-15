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

def usgs_japon_json_etl(url, filename, format=None):
    
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
    # df_sismo.to_json(path_or_buf= '../DASHBOARD/CSV_ORIGINAL/' + filename, orient="records")
    
    # Devolver el DataFrame
    return df_sismo.to_csv(path_or_buf= '../DASHBOARD/CSV_ORIGINAL/' + filename, index=False)