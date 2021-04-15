from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

dag = DAG(
    dag_id='simple_dag',
    schedule_interval='*/10 * * * *',
    start_date=days_ago(2),
    catchup=False
)

hello_task = BashOperator(
    task_id='say_hello',
    bash_command='echo Hello',
    dag=dag,
)
