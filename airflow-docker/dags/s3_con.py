# source_bucket_key = 's3://data-lake-sismos/sin-etl/sismos_usa.json'
#
"""
S3 Sensor Connection Test
"""

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
# from airflow.providers.amazon.aws.operators.s3 import S3FileTransformOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('s3_dag_test', default_args=default_args, schedule_interval= '@once')

def print_message():
    print("Hello, it should work")

t1 = PythonOperator(
    task_id='print_message',
    python_callable=print_message,
    dag=dag
)

sensor = S3KeySensor(
    task_id='check_s3_for_file_in_s3',
    bucket_key=f's3://data-lake-sismos/sin-etl/sismos_usa.json',
    bucket_name=None,
    aws_conn_id='my_conn_S3',
    timeout=18*60*60,
    poke_interval=120,
    dag=dag)


t1.set_upstream(sensor)
