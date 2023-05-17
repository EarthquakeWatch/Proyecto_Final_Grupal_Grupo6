import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
from datetime import datetime, timedelta
from IPython.display import display
# Limit to events with a specific PAGER alert level. The allowed values are:
# alertlevel=green
# Limit to events with PAGER alert level "green".
# alertlevel=yellow
# Limit to events with PAGER alert level "yellow".
# alertlevel=orange
# Limit to events with PAGER alert level "orange".
# alertlevel=red
# Limit to events with PAGER alert level "red".

def usgs_json_raw(url, filename, pais, format=None, alertlevel=None):
    """
    Función para obtener datos de sismos de la API de USGS y guardarlos en un archivo CSV.
    
    Args:
        url (str): URL de la API de USGS.
        filename (str): Nombre del archivo CSV de salida.
        pais (str): País para filtrar los sismos.
        format (str, optional): Formato de los datos. Por defecto, None.
        alertlevel (bool, optional): Indicador para concatenar todas las alertas. Por defecto, None.
    
    Returns:
        DataFrame: DataFrame con los datos de los sismos.
    """
    # Establecer el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=20000)).strftime('%Y-%m-%dT%H:%M:%S')
    # starttime = (datetime.today() - timedelta(days=50*365)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Definir los límites geográficos según el país
    dic = {
        "peru": {"minlatitude": -18.521, "maxlatitude": 0.132, "minlongitude": -84.419, "maxlongitude": -68.599},
        "usa": {"minlatitude": 24.6, "maxlatitude": 50, "minlongitude": -125, "maxlongitude": -65},
        "japon": {"minlatitude": 24.40, "maxlatitude": 45, "minlongitude": 122.93, "maxlongitude": 153.99}
    }
    values = dic[pais]
    minlatitude = values["minlatitude"]
    maxlatitude = values["maxlatitude"]
    minlongitude = values["minlongitude"]
    maxlongitude = values["maxlongitude"]
    
    # Configurar los parámetros de la solicitud
    params = {
        "format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
        "minlatitude": minlatitude, "maxlatitude": maxlatitude, "minlongitude": minlongitude,
        "maxlongitude": maxlongitude, "limit": 20000
    }
    dfs = []
    if alertlevel:
        # Obtener los niveles de alerta disponibles
        alert_levels = ["green", "yellow", "orange", "red"]
        
        for level in alert_levels:
            params["alertlevel"] = level
            response = requests.get(url, params=params)
            data = response.json()
            features = data['features']
            df_sismo = pd.json_normalize(features)
            df_sismo["properties.time"] = pd.to_datetime(df_sismo["properties.time"], unit="ms")
            df_sismo["properties.updated"] = pd.to_datetime(df_sismo["properties.updated"], unit="ms")
            df_sismo[["Longitud", "Latitud", "Profundidad"]] = pd.DataFrame(df_sismo["geometry.coordinates"].tolist())
            dfs.append(df_sismo)
    else:
        # Realizar la solicitud a la API de USGS sin niveles de alerta como parametro condicional
        for _ in range(8):
            response = requests.get(url, params=params)
            data = response.json()
            features = data['features']
            df_sismo = pd.json_normalize(features)
            df_sismo["properties.time"] = pd.to_datetime(df_sismo["properties.time"], unit="ms")
            df_sismo["properties.updated"] = pd.to_datetime(df_sismo["properties.updated"], unit="ms")
            df_sismo[["Longitud", "Latitud", "Profundidad"]] = pd.DataFrame(df_sismo["geometry.coordinates"].tolist())
            # Concatenar los nuevos datos al DataFrame existente
            dfs.append(df_sismo)
            display(df_sismo["properties.time"].min())
            # Obtener el valor mínimo de 'properties.time' en el DataFrame actual
            min_time = df_sismo["properties.time"].min()
            # Convertir el valor mínimo en formato de fecha y hora
            new_endttime = min_time.strftime('%Y-%m-%dT%H:%M:%S')
            # Actualizar el parámetro 'starttime' en los parámetros de solicitud
            params["endtime"] = new_endttime
        # Combinar todos los DataFrames
        df_sismo = pd.concat(dfs)

    # Guardad el DataFrame en un archivo CSV
    # df_sismo.to_csv(path_or_buf='../DASHBOARD/CSV_ORIGINAL/' + filename, index=False)
    df_sismo.to_csv(path_or_buf='../MACHINE_LEARNING/' + filename, index=False)
    display(df_sismo.shape)
    return df_sismo

url = r'https://earthquake.usgs.gov/fdsnws/event/1/query?'

# usgs_json_raw(url, 'raw_alert_usa.csv', "usa", alertlevel=True)
# usgs_json_raw(url, 'raw_alert_japon.csv', "japon", alertlevel=True)
usgs_json_raw(url, 'raw_usa.csv', "usa", alertlevel=None)
