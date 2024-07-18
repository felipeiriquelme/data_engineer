from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago

# Define los argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define el DAG
dag = DAG(
    'gcs_to_bigquery_dag',
    default_args=default_args,
    description='DAG triggered by GCS file upload to load data into BigQuery',
    schedule_interval=None,  # No schedule, trigger by events
    start_date=days_ago(1),
    catchup=False,
)

# Define la tarea para cargar el archivo de GCS a BigQuery
gcs_to_bigquery = GCSToBigQueryOperator(
    task_id='load_gcs_to_bigquery',
    bucket='wom-bucket',
    source_objects=['path/to/your/file.csv'],
    destination_project_dataset_table='a.b.c',
    schema_fields=[
        {'name': 'field1', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'field2', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        # Define los campos de tu esquema aquí
    ],
    write_disposition='WRITE_TRUNCATE',
    dag=dag,
)

# Define el flujo de trabajo
gcs_to_bigquery
