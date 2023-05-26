from airflow import DAG
from airflow.providers.amazon.aws.operators.lambda_function import LambdaInvokeFunctionOperator
from airflow.providers.amazon.aws.operators.ec2 import EC2StartInstanceOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'my_lambda_dag',
    default_args=default_args,
    description='DAG para invocar función Lambda diariamente',
    schedule_interval='@daily',
) as dag:
    invoke_lambda_function = LambdaInvokeFunctionOperator(
        task_id="invoke_api_request_function",
        function_name="api-autom",
        log_type="Tail",
        invocation_type="RequestResponse",
        aws_conn_id="my_conn_S3"
    )

    transform_task = LambdaInvokeFunctionOperator(
        task_id="invoke_transform_function",
        function_name="transform",
        log_type="Tail",
        invocation_type="RequestResponse",
        aws_conn_id="my_conn_S3"
    )

    # Operador para iniciar la instancia EC2
    start_instance_task = EC2StartInstanceOperator(
        task_id="iniciar_instancia_ec2",
        instance_id="i-0cab4ca758666c80a",
        aws_conn_id="my_conn_S3",
        region_name="sa-east-1",
        dag=dag
    )

invoke_lambda_function >> transform_task >> start_instance_task