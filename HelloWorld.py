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


"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
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
    # 'queue': 'bash_queue',
     'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'tutorial', default_args=default_args, schedule_interval=timedelta(days=1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t1)
