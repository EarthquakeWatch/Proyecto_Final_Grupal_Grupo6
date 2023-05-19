# %%
import mysql.connector
import pandas as  pd
import csv

# %%
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="SISMOS"
)


# %%
cursor = conexion.cursor()

# %%
archivo_csv = 'DASHBOARD/CSV_TRANSFORMADOS/Datos_USA.csv'
tabla = 'USA'

with open(archivo_csv, 'r') as archivo:
    lector_csv = csv.reader(archivo)
    encabezado = next(lector_csv)  # Leer la primera línea como encabezado

    for fila in lector_csv:
        columnas = ', '.join([f"`{col}`" for col in encabezado])
        valores = ', '.join(['%s'] * len(encabezado))
        consulta = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})"
        cursor.execute(consulta, fila)

conexion.commit()  # Confirmar los cambios en la base de datos


# %%
archivo_csv = 'DASHBOARD/CSV_TRANSFORMADOS/Datos_Japon.csv'
tabla = 'JAPON'

with open(archivo_csv, 'r',encoding='utf-8') as archivo:
    lector_csv = csv.reader(archivo)
    encabezado = next(lector_csv)  # Leer la primera línea como encabezado

    for fila in lector_csv:
        columnas = ', '.join([f"`{col}`" for col in encabezado])
        valores = ', '.join(['%s'] * len(encabezado))
        consulta = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})"
        cursor.execute(consulta, fila)

conexion.commit()  # Confirmar los cambios en la base de datos

# %%
archivo_csv = 'DASHBOARD/CSV_TRANSFORMADOS/Datos_Peru_USGS.csv'
tabla = 'PERU'

with open(archivo_csv, 'r',encoding='utf-8') as archivo:
    lector_csv = csv.reader(archivo)
    encabezado = next(lector_csv)  # Leer la primera línea como encabezado

    for fila in lector_csv:
        columnas = ', '.join([f"`{col}`" for col in encabezado])
        valores = ', '.join(['%s'] * len(encabezado))
        consulta = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})"
        cursor.execute(consulta, fila)

conexion.commit()  # Confirmar los cambios en la base de datos

# %%
conexion.close()  # Cerrar la conexión a la base de datos


