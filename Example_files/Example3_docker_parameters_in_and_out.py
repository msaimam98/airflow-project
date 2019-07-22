from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
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
    'retry_delay': timedelta(minutes=5)
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


def print11(**kwargs):
    first = kwargs['templates_dict']['a3']
    print(first)
    return first

t1 = DockerOperator(
    task_id='divide1_conv_on',
    image='useful1',
    command='5 6',
    xcom_push=True,
    dag=dag)

t2 = PythonOperator(
    task_id='print_task',
    python_callable=print11,
    provide_context=True,
    xcom_push=True,
    templates_dict={
        'a3': "{{ ti.xcom_pull(task_ids='divide1_conv_on')}}" },
    dag=dag
)

t3 = DockerOperator(
    task_id='docker2',
    image='useful1',
    command="{{ ti.xcom_pull(task_ids='print_task')}}" + ' 10',
    xcom_push=True,
    dag=dag)

t4 = PythonOperator(
    task_id='print_task2',
    python_callable=print11,
    provide_context=True,
    xcom_push=True,
    templates_dict={
        'a3': "{{ ti.xcom_pull(task_ids='docker2')}}" },
    dag=dag )

t2.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)
