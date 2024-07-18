# dag.py

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': "felipeiriquelmeespinoza@gmail.com",
    'email_on_retry': "felipeiriquelmeespinoza@gmail.com",
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'wom-dag',
    default_args=default_args,
    description='Process WOM CSV file and load into BigQuery',
    schedule_interval=None,
)

def my_task():
    # Aquí va la lógica de tu tarea
    pass

task1 = PythonOperator(
    task_id='task1',
    python_callable=my_task,
    dag=dag,
)


