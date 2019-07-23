from typing import Optional

"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'pool': 'backfill'
    # 'queue': 'bash_queue',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('tut', default_args=default_args, schedule_interval=timedelta(days=1))

ON_CALLS = 1000
OFF_CALLS = 1000
ON_SALES = 50
OFF_SALES = 40


# def print11(**kwargs):
#     first = kwargs['templates_dict']['a3']
#     print(first)

t1 = DockerOperator(
    task_id='divide1_conv_on',
    image='useful2',
    command='divide '+ str(ON_SALES) + ' ' + str(ON_CALLS),
    xcom_push=True,
    dag=dag)

t2 = DockerOperator(
    task_id='divide1_conv_off',
    image='useful2',
    command='divide ' + str(OFF_SALES) + ' ' + str(OFF_CALLS),
    xcom_push=True,
    dag=dag)


t3 = DockerOperator(
    task_id='numerator',
    image='useful2',
    command='subtract ' + "{{ti.xcom_pull(task_ids='divide1_conv_on')}}" +
            ' ' + "{{ti.xcom_pull(task_ids='divide1_conv_off')}}",
    xcom_push=True,
    dag=dag)

t4 = DockerOperator(
    task_id='divide_results',
    image='useful2',
    command='divide ' + "{{ti.xcom_pull(task_ids='numerator')}}" +
            ' ' + "{{ti.xcom_pull(task_ids='divide1_conv_off')}}",
    xcom_push=True,
    dag=dag)


t3.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)
