# from airflow import DAG
# from airflow.sensors.external_task import ExternalTaskSensor
# from airflow.providers.amazon.aws.operators.lambda_function import LambdaInvokeFunctionOperator
# from datetime import datetime
# from datetime import timedelta
# from airflow.utils.dates import days_ago

# default_args = {
#     'owner': 'airflow',
#     'start_date': days_ago(1),
#     'retries': 0,
#     'retry_delay': timedelta(minutes=5),
# }
# with DAG('transform_dag', default_args=default_args, schedule_interval=None) as dag:
    
#     wait_task = ExternalTaskSensor(
#         task_id='wait_lamba_dag',
#         external_dag_id='my_lamba_dag',
#         # external_task_id=''
#         # execution_date="{{ dag_run.conf['execution_date'] }}"

#     )

#     transform_task = LambdaInvokeFunctionOperator(
#         task_id="invoke_lambda_function",
#         function_name="transforrm",
#         log_type="Tail",
#         invocation_type="RequestResponse",
#         aws_conn_id="my_conn_S3"
#     )
    
#     wait_task >> transform_task
