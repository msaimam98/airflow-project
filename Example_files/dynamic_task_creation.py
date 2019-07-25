#
# import logging
# import pandas as pd
# import airflow
from airflow import DAG
from airflow.utils import dates as date
from datetime import timedelta, datetime
# from airflow.operators.dummy_operator import DummyOperator
# from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
# from airflow.utils.decorators import apply_defaults
from airflow.operators.docker_operator import DockerOperator
import json


#
""" define DAG arguments which can be override on a per-task basis during operator initialization """
default_args = {
  'owner': 'Tom',
  'depends_on_past': False,
  'start_date': datetime(2018, 4, 15),
  'email': ['tom-kun@gmail.com'],
  'email_on_failure': True,
  'email_on_retry': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=5),
  'provide_context': True # Provide_context is required when we're using XComs Airflow's concept to push and pull function results into an other task.
}
#
#
#
# def get_tables(table_file="/tmp/daily", **kwargs):
#     logging.info("######## Starting get_tables() function ########")
#     logging.info("######## Load the table file into a new Pandas DataFrame ########")
#     df_tables = pd.read_csv(table_file, names=["TABLES"])
#     df_tables["TABLES"] = df_tables["TABLES"].str.strip()
#     lst_tables_sqoop = df_tables["TABLES"].tolist()
#     return lst_tables_sqoop
#
dag = DAG('docker_file1', default_args=default_args,
          schedule_interval=timedelta(days=1))

ON_CALLS = 1000
OFF_CALLS = 1000
ON_SALES = 50
OFF_SALES = 40

with open('/usr/local/airflow/dags/format.json') as g:
    data = json.load(g)


# def mapping(dict, dag1):
#
#     if not dict['ttl']:
#         t1 = DockerOperator(
#             task_id=dict['task_id'],
#             dag=dag1)
#         return t1
#     else:
#         list_to_edit = []
#         for task in dict['ttl']:
#             list_to_edit.extend(mapping(task, dag))
#         t = DockerOperator(
#             task_id=dict['task_id'],
#             dag=dag1)
#         final = [t]
#         final.extend(list_to_edit)
#         for i in range(len(list_to_edit)):
#             t.set_upstream(list_to_edit[i])
#         return final

def mapping(dict, dag1):

    if not dict['ttl']:
        if bool(dict["eval_command"]) == True:
            t1 = DockerOperator(
                task_id=dict['task_id'],
                image=dict['image'],
                command=exec(dict['command']),
                xcom_push=bool(dict['xcom_push']),
                dag=dag1)
            return [t1]
        else:
            t1 = DockerOperator(
                task_id=dict['task_id'],
                image=dict['image'],
                command=dict['command'],
                xcom_push=bool(dict['xcom_push']),
                dag=dag1)
            return [t1]

    else:
        list_to_edit = []
        for task in dict['ttl']:
            list_to_edit.extend(mapping(task, dag))
        t = DockerOperator(
            task_id=dict['task_id'],
            image=dict['image'],
            command=dict['command'],
            xcom_push=bool(dict['xcom_push']),
            dag=dag1)
        final = [t]
        final.extend(list_to_edit)
        for i in range(len(list_to_edit)):
            t.set_upstream(list_to_edit[i])
        return [t]

return1 = mapping(data, dag)
print(return1)

# if __name__ == "__main__":
#     print(data)
#     return1 = mapping(data, dag)
#     print(return1)


# let the function print the json format to see the right input

# testing is very important - test as you go

# first without airflow - parsing is priority

# generate memory objects


# def mapping(dict):
#
#
#     if not dict['ttl']:
#         newnew = []
#         for key in dict.keys():
#             if key is not 'ttl':
#                 if key is task or fegerg or e rg or  reg:
#                 newnew.append((key, dict[key])
#         t1 = DockerOperator(
#             task_id=dict['task_id'],
#             newnew[1][0] = newnew[1][1],
#             newnew[2][0] = newnew[2][1],
#             newnew[3][0] = newnew[3][1],
#             newnew[4][0] = newnew[4][1])
#         return t1
#     else:
#         list_to_edit = []
#         for task in dict['ttl']:
#             list_to_edit.append(mapping(task))
#         list_to = []
#         for key in dict.keys():
#             if key is not dict['ttl']:
#                 list_to.append((key, dict[key])
#         t = DockerOperator(
#             newnew[0][0]=newnew[0][1],
#             newnew[1][0] = newnew[1][1],
#             newnew[2][0] = newnew[2][1],
#             newnew[3][0] = newnew[3][1],
#             newnew[4][0] = newnew[4][1])
#         strr =
#         for i in range(len(list_to_edit))):
#
