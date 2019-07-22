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

dag = DAG('calc_draft_1', default_args=default_args, schedule_interval=timedelta(days=1))

ON_CALLS = 1000
OFF_CALLS = 1000
ON_SALES = 50
OFF_SALES = 40


# def on_conversion(on_calls, on_sales):
#     """ """
#     return (on_sales/on_calls) * 100
#
#
# def off_conversion(off_calls, off_sales):
#     """ """
#     return (off_sales/off_calls) * 100
#
#
# def numerat(**kwargs):
#     """ """
#     ti = kwargs['ti']
#     print(ti)
#     on_cr = ti.xcom_pull(task_ids='convert_to_on')
#     off_cr = ti.xcom_pull(task_ids='convert_to_off')
#     return on_cr - off_cr
#
#
# def divide(**kwargs):
#     """ """
#     ti = kwargs['ti']
#     nume = ti.xcom_pull(task_ids='numerator')
#     denom = ti.xcom_pull(task_ids='convert_to_off')
#     return (nume/denom) * 100


def divide(**kwargs):
    num = kwargs['templates_dict']['a3']
    denom = kwargs['templates_dict']['b3']
    # if isinstance(num1, int):
    #     num = num1
    # if isinstance(denom1, int):
    #     denom = denom1
    return float(num)/float(denom)


def add(**kwargs):
    first = kwargs['templates_dict']['a3']
    second = kwargs['templates_dict']['b3']
    # if isinstance(first1, int):
    #     first = first1
    # if isinstance(second1, int):
    #     second = second1
    return float(first) + float(second)


def subtract(**kwargs):
    big = kwargs['templates_dict']['a3']
    small = kwargs['templates_dict']['b3']
    # if isinstance(big1, int):
    #     big = big1
    # if isinstance(small1, int):
    #     small = small1
    return float(big) - float(small)


def multiply(**kwargs):
    first = kwargs['templates_dict']['a3']
    second = kwargs['templates_dict']['b3']
    # if isinstance(first1, int):
    #     first = first1
    # if isinstance(second1, int):
    #     second = second1
    return float(first) * float(second)


t1 = PythonOperator(
    task_id='convert_to_on',
    python_callable=divide,
    provide_context=True,
    templates_dict={
        'a3': ON_SALES,
        'b3': ON_CALLS},
    dag=dag)

OFF_SALES = 50

t2 = PythonOperator(
    task_id='convert_to_off',
    python_callable=divide,
    provide_context=True,
    templates_dict={
        'a3': OFF_SALES,
        'b3': OFF_CALLS},
    dag=dag)

# OFF_SALES = 50

t3 = PythonOperator(
    task_id='numerator',
    python_callable=subtract,
    provide_context=True,
    templates_dict={
        'a3': "{{ ti.xcom_pull(task_ids='convert_to_on') }}",
        'b3': "{{ ti.xcom_pull(task_ids='convert_to_off') }}"}
    ,
    dag=dag)

t4 = PythonOperator(
    task_id='divide1',
    python_callable=divide,
    provide_context=True,
    templates_dict={
        'a3': "{{ ti.xcom_pull(task_ids='numerator') }}",
        'b3': "{{ ti.xcom_pull(task_ids='convert_to_off') }}"},
    dag=dag
)

t1.set_downstream(t3)
t2.set_downstream(t3)
t3.set_downstream(t4)


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
