import os
import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'email': os.environ['FAILURE_EMAIL'],
    'start_date': days_ago(0),
    'email_on_failure': True,
}

dag = DAG(
    dag_id='games', 
    default_args=default_args, 
    schedule_interval="* * * * *"
)

t1 = BashOperator(
    task_id='sklearn_pipeline',
    bash_command='sudo docker run sklearn_pipeline',
    dag=dag
)
