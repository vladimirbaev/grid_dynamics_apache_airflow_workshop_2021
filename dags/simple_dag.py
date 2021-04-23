import json
import os
from datetime import datetime

from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule


def toss_a_coin_fn():
    from random import choice
    return choice(['feeling_lucky', 'no_launch'])


def is_weather_suitable_fn(ti=None, **_):
    response = json.loads(ti.xcom_pull(task_ids='get_weather_data'))
    if response['current']['clouds'] > 80:
        return 'toss_a_coin'
    return 'weather_is_suitable'


def on_success_cb(context):
    from hooks.telegram_hook import TelegramHook
    message = f'The rocket has been launched! execution_date = {context["execution_date"]}'
    hook = TelegramHook('telegram')
    hook.run(message)


with DAG(
    dag_id='space_x_rocket_launcher',
    schedule_interval=None,
    start_date=datetime(2021, 4, 1),
    max_active_runs=1,
    catchup=False
) as dag:
    get_weather_data = SimpleHttpOperator(
        task_id='get_weather_data',
        method='GET',
        endpoint='/data/2.5/onecall',
        data={
            'lat': 60,
            'lon': 30,
            'appid': os.environ['WEATHER_API_KEY']
        },
        xcom_push=True
    )

    is_weather_suitable = BranchPythonOperator(
        task_id='is_weather_suitable',
        python_callable=is_weather_suitable_fn,
        provide_context=True
    )

    weather_is_suitable = DummyOperator(
        task_id='weather_is_suitable'
    )

    toss_a_coin = BranchPythonOperator(
        task_id='toss_a_coin',
        python_callable=toss_a_coin_fn
    )

    feeling_lucky = DummyOperator(
        task_id='feeling_lucky'
    )

    prepare_for_the_launch = BashOperator(
        task_id='prepare_for_the_launch',
        bash_command='echo Preparing trampoline',
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    launch_the_rocket = PostgresOperator(
        task_id='launch_the_rocket',
        postgres_conn_id='postgres_default',
        sql="""
            insert into launch_status (execution_ts, status) values
            ( '{{ ts }}', 'Success' )
        """,
        on_success_callback=on_success_cb
    )

    no_launch = BashOperator(
        task_id='no_launch',
        bash_command='echo Go home',
    )

    wait_for_approval = FileSensor(
        task_id='wait_for_approval',
        filepath='/opt/airflow/files/approved',
        poke_interval=1,
    )

    wait_for_approval >> get_weather_data >> is_weather_suitable

    is_weather_suitable >> [toss_a_coin, weather_is_suitable]
    toss_a_coin >> [feeling_lucky, no_launch]

    [feeling_lucky, weather_is_suitable] >> prepare_for_the_launch

    prepare_for_the_launch >> launch_the_rocket
