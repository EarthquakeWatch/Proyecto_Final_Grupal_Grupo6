import json  # proporciona métodos para trabajar con datos JSON.
import os  # proporciona una manera de utilizar las funcionalidades dependientes del sistema operativo, como leer o escribir archivos.
import boto3  # biblioteca de AWS (Amazon Web Services) para Python, que permite interactuar con los servicios de AWS, como S3.
import requests  # permite enviar solicitudes HTTP/1.1 muy fácilmente.
from datetime import datetime, timedelta  #datetime proporciona clases para trabajar con fechas y tiempos. 
from botocore.exceptions import ClientError  # es la biblioteca base para interactuar con los servicios de AWS en Python. 
# ClientError es una excepción que se utiliza para manejar errores relacionados con las solicitudes de clientes a los servicios de AWS.

# lambda_handler es la función principal de la función Lambda. Recibe dos parámetros: event, que contiene información sobre el evento 
# que activó la función Lambda, y context, que contiene información sobre el entorno de ejecución de la función Lambda.
def lambda_handler(event, context):
    url = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"

    # Establece el tiempo de inicio desde hoy menos 20000 eventos
    endtime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    starttime = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')

    # Establece los demás parámetros de solicitud
    params = {"format": "geojson", "starttime": starttime, "endtime": endtime, "minmagnitude": 2.5,
                "minlatitude": 24.6, "maxlatitude": 50, "minlongitude": -125, "maxlongitude": -65, "limit": 20000}

    # Realiza la solicitud a la API de USGS
    data = requests.get(url, params=params)
    data = data.json()

    # Guarda los eventos en un archivo JSON en un bucket S3
    # s3 = boto3.client('s3')
    bucket = 'data-lake-sismos'  # Reemplaza con el nombre de tu bucket
    foldername = 'sin-etl'
    filename = f'{foldername}/sismos_usa.json'
    # s3.put_object(Bucket=bucket_name, Key=filename, Body=json.dumps(data))
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        with open('/tmp/sismos_usa.json', 'w') as file:
            json.dump(data, file)
        response = s3_client.upload_file('/tmp/sismos_usa.json', bucket, filename)
    except ClientError as e:
        logging.error(e)
        return False
    return {
        'statusCode': 200,
        'body': json.dumps('Sismos guardados en S3')
    }
