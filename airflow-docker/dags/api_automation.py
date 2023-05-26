# from datetime import datetime, timedelta
# import json
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from usa_json_etl import sismo_usa_json_etl
# from Mongodb import insert_single_document

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2023, 5, 14),
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5)
# }

# dag = DAG('sismo_usa_json_etl_dag', default_args=default_args, schedule_interval='0 0 * * *')

# def sismo_usa_json_etl_task():
#     url = r"https://earthquake.usgs.gov/fdsnws/event/1/query?"
#     filename = "sismo_usa_data.json"
#     return sismo_usa_json_etl(url, filename)

# def insert_mongo(ti):
#     json_file_path = ti.xcom_pull(task_ids='request_etl')
#     try:
#         with open(json_file_path) as file:
#             json_content = file.read()
#             json_data = json.loads(json_content)
#             insert_single_document("config", json_data)
#             print("Archivo JSON guardado correctamente")
#     except json.JSONDecodeError:
#         print("Invalid JSON format")

# request_etl = PythonOperator(
#     task_id='request_etl',
#     python_callable=sismo_usa_json_etl_task,
#     dag=dag
# )

# insert_mongo = PythonOperator(
#     task_id='insert_mongo',
#     python_callable=insert_mongo,
#     dag=dag
# )


# request_etl >> insert_mongo