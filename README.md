# airflow-project

## How to initialise an airflow container with a working DAG 


- docker run -d -p 8088:8080 -v ~/path/to/folder/with/Helloworld.py:/usr/local/airflow/dags puckel/docker-airflow webserver
  - This opens up a container with host port 8088 connected to the container at port 8080
  - This container has a volume mounted onto it that includes the python script with all tasks in the DAG
  - This container opens up a webserver to visualise and keep track of the DAG
## How to get into the container and test the DAG and its tasks out 

- docker exec -ti <container_name> bash\
After this command, we will be put into the container while its up and running 

- To test the tasks out, we will use the airflow test command
   - airflow test [DAG_id] [task_id] [any_date_in_the_past]
     - Running this in the container should give us the output we have specified in the task
     - The airflow test command runs task instances locally, outputs their log to stdout (on screen), doesn’t bother with dependencies, and doesn’t communicate state (running, success, failed, …) to the database

- To test the DAG and have the results show on the webserver, we will use the airflow backfill command
  - airflow backfill [DAG_id] -s [START_DATE] -e [END_DATE]
    - The airflow backfill command will respect your dependencies, emit logs into files and talk to the database to record status. 
    - If you do have a webserver up, you’ll be able to track the progress
