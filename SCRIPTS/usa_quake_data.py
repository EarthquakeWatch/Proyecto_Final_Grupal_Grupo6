#Este código en Python utiliza las bibliotecas requests, json, pandas, folium y numpy para obtener datos sobre terremotos 
#en los Estados Unidos, convertirlos en un objeto de marco de datos de Pandas y mostrarlos en un mapa utilizando Folium

import requests  # importa la biblioteca requests que se usa para hacer solicitudes HTTP a una URL.
import json  # importa la biblioteca json que se usa para trabajar con datos JSON.
import pandas as pd  # importa la biblioteca pandas como pd, que se utiliza para trabajar con marcos de datos.
import numpy as np  # importa la biblioteca numpy como np, que se utiliza para realizar operaciones matemáticas en matrices y arreglos de datos.

def sismo_usa(url):
    paramss = {"format": "geojson", "starttime": "1995-01-01", "endtime": "2023-01-01", "minmagnitude": 2.5,
                "minlatitude": 24.6, "maxlatitude": 50, "minlongitude": -125, "maxlongitude": -65, "limit": 20000}
    data = requests.get(url, params = paramss)
    data = json.loads(data.text)
    return data
#se define una función llamada sismo_usa que acepta una URL como entrada. La función utiliza la biblioteca requests para hacer 
#una solicitud HTTP GET a la URL proporcionada, pasando algunos parámetros específicos en la variable paramss. 
#Luego, la respuesta se analiza como JSON utilizando la biblioteca json y se devuelve.

url = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"
dic_sismo = sismo_usa(url)
#se define una URL que apunta al servicio web del USGS que proporciona información sobre terremotos en los Estados Unidos. 
#Luego, se llama a la función sismo_usa y se le pasa la URL como argumento. El objeto JSON devuelto por la función se almacena 
#en la variable dic_sismo.

df_sismo = pd.json_normalize(dic_sismo['features'])
#se utiliza la biblioteca pandas y la función json_normalize para convertir el objeto JSON devuelto por la función sismo_usa 
# en un DataFrame de pandas. Esto facilita la manipulación y el análisis de los datos.