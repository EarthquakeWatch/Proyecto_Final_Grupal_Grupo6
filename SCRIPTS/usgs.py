import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
from datetime import datetime, timedelta
#Peru
#[-18.521, 0.132] Latitude
#[-84.419, -68.599] Longitude

def usgs_peru_json_raw(url, filename, format=None):
    
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Establecer los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": -18.521, "maxlatitude": 0.132, "minlongitude": -84.419, "maxlongitude": -68.599, "limit": 20000}
    
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
    
    # df_sismo.drop(columns=[])
    
    # df_sismo.drop(columns=['type',"properties.tz",'properties.tz', 'properties.code','properties.url',
    #                        'properties.detail','properties.alert', 'properties.status','properties.types','properties.sources','properties.magType',
    #                        'properties.type', 'properties.title', 'geometry.type'], axis=1, inplace=True)
    # Renombrar las columnas
    # df_sismo = df_sismo.rename(columns={"properties.mag": "Magnitud",
    #                                     "properties.time": "Primer Registro",
    #                                     "properties.updated": "Último Registro",
    #                                     "properties.place": "Ubicación",
    #                                     "Longitud": "Longitud (grados)",
    #                                     "Latitud": "Latitud (grados)",
    #                                     "Profundidad": "Profundidad (km)"})
    
    # Guardar el DataFrame en un archivo JSON
    # df_sismo.to_json(path_or_buf= '../DASHBOARD/CSV_ORIGINAL/' + filename, orient="records")
    
    # Devolver el DataFrame
    return df_sismo.to_csv(path_or_buf= '../DASHBOARD/CSV_ORIGINAL/' + filename, index=False)

url = r'https://earthquake.usgs.gov/fdsnws/event/1/query?'
filename = 'raw_usgs_peru.csv'

usgs_peru_json_raw(url, filename)

