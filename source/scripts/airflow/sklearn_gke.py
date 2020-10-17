import os
import datetime

from airflow import DAG
from airflow.contrib.operators.gcp_container_operator import GKEPodOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'email': os.environ['GOOGLE_FAILURE_EMAIL'],
    'start_date': days_ago(0),
    'email_on_failure': True,
}

dag = DAG(
    dag_id='games_docker', 
    default_args=default_args, 
    schedule_interval="* * * * *"
)

t1 = GKEPodOperator(
    task_id='sklearn_pipeline',
    project_id=os.environ['GOOGLE_PROJECT_ID'],
    cluster_name=os.environ['GOOGLE_GKE_CLUSTER_NAME'],
    name='sklearn-pipeline',
    namespace='default',
    location=os.environ['GOOGLE_GKE_CLUSTER_LOCATION'],
    image=f"us.gcr.io/{os.environ['GOOGLE_PROJECT_ID']}/sklearn_pipeline",
    dag=dag
)
