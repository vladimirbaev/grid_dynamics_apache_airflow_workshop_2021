from datetime import datetime
from random import choice

# noinspection PyPackageRequirements
from airflow import DAG
# noinspection PyDeprecation
# noinspection PyPackageRequirements
from airflow.contrib.sensors.file_sensor import FileSensor
# noinspection PyDeprecation
# noinspection PyPackageRequirements
from airflow.operators.bash_operator import BashOperator
# noinspection PyDeprecation
# noinspection PyPackageRequirements
from airflow.operators.python_operator import BranchPythonOperator

dag = DAG(
    dag_id='space_x_rocket_launcher',
    schedule_interval=None,
    start_date=datetime(2021, 4, 1),
    max_active_runs=1,
    catchup=False
)

# start_date: 2021, April, 1st, @daily
# 1. when the first dag run is going to happen?
# 00:00, start_date + schedule_interval


def toss_a_coin_fn():
    return choice(['prepare_for_the_launch', 'no_launch'])

toss_a_coin = BranchPythonOperator(
    task_id='toss_a_coin',
    python_callable=toss_a_coin_fn
)

prepare_for_the_launch = BashOperator(
    task_id='prepare_for_the_launch',
    bash_command='echo Preparing trampoline; sleep 10;',
    dag=dag,
)

launch_the_rocket = BashOperator(
    task_id='launch_the_rocket',
    bash_command='echo Launching the rocket',
    dag=dag,
)

no_launch = BashOperator(
    task_id='no_launch',
    bash_command='echo Go home',
    dag=dag,
)

# prepare_for_the_launch.set_downstream(launch_the_rocket) == launch_the_rocket.set_upstream(prepare_for_the_launch)
# launch_the_rocket << prepare_for_the_launch

# poke()
# poke_interval
# mode = ['poke', 'reschedule', 'smart_sensor']
wait_for_approval = FileSensor(
    task_id='wait_for_approval',
    filepath='/opt/airflow/files/approved',
    poke_interval=1,
    dag=dag,
)

wait_for_approval >> toss_a_coin >> [prepare_for_the_launch, no_launch]
prepare_for_the_launch >> launch_the_rocket
