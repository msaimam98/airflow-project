# from airflow import DAG
# from airflow.operators import BashOperator
# from datetime import datetime, timedelta
#
# # Following are defaults which can be overridden later on
# default_args = {
#     'owner': 'manasi',
#     'depends_on_past': False,
#     'start_date': datetime(2016, 4, 15),
#     'email': ['manasidalvi14@gmail.com'],
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=1),
# }
#
# dag = DAG('Helloworld', default_args=default_args)
#
# # t1, t2, t3 and t4 are examples of tasks created using operators
#
# t1 = BashOperator(
#     task_id='task_1',
#     bash_command='echo "Hello World from Task 1"',
#     dag=dag)
#
# t2 = BashOperator(
#     task_id='task_2',
#     bash_command='echo "Hello World from Task 2"',
#     dag=dag)
#
# t3 = BashOperator(
#     task_id='task_3',
#     bash_command='echo "Hello World from Task 3"',
#     dag=dag)
#
# t4 = BashOperator(
#     task_id='task_4',
#     bash_command='echo "Hello World from Task 4"',
#     dag=dag)
#
# t2.set_upstream(t1)
# t3.set_upstream(t1)
# t4.set_upstream(t2)
# t4.set_upstream(t3)
#
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
    command='divide {{ ON_SALES }} {{ ON_CALLS }}',
    xcom_push=True,
    dag=dag)

t2 = DockerOperator(
    task_id='divide1_conv_off',
    image='useful2',
    command='divide "{{ OFF_SALES }}" "{{ OFF_CALLS }}"',
    xcom_push=True,
    dag=dag)


t3 = DockerOperator(
    task_id='numerator',
    image='useful2',
    command='subtract "{{ ti.xcom_pull(task_ids=\'divide1_conv_on\') }}" "{{ ti.xcom_pull(task_ids=\'divide1_conv_off\') }}"',
    xcom_push=True,
    dag=dag)

t4 = DockerOperator(
    task_id='divide_results',
    image='useful2',
    command='divide "{{ ti.xcom_pull(task_ids=\'numerator\') }}" "{{ ti.xcom_pull(task_ids=\'divide_conv_off\') }}"',
    xcom_push=True,
    dag=dag)



# t2 = DockerOperator(
#     task_id='print_task',
#     python_callable=print11,
#     provide_context=True,
#     templates_dict={
#         'a3': "{{ ti.xcom_pull(task_ids='divide1_conv_on') }}"},
#     dag=dag)

t3.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)


# # t1, t2 and t3 are examples of tasks created by instantiating operators
# t1 = BashOperator(
#     task_id='print_date',
#     bash_command='date',
#     dag=dag)
#
# t2 = BashOperator(
#     task_id='sleep',
#     bash_command='sleep 5',
#     retries=3,
#     dag=dag)
#
# templated_command = """
#     {% for i in range(5) %}
#         echo "{{ ds }}"
#         echo "{{ macros.ds_add(ds, 7)}}"
#         echo "{{ params.my_param }}"
#     {% endfor %}
# """
#
# t3 = BashOperator(
#     task_id='templated',
#     bash_command=templated_command,
#     params={'my_param': 'Parameter I passed in'},
#     dag=dag)
#
# t2.set_upstream(t1)
# t3.set_upstream(t1)
