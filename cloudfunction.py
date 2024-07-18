import base64
import json
import requests
from google.cloud import pubsub_v1

def trigger_airflow_dag(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_data = json.loads(pubsub_message)
    # Parse message data to get bucket and file info if needed

    # Endpoint de Airflow para ejecutar el DAG
    airflow_endpoint = 'http://your-airflow-webserver:8080/api/v1/dags/gcs_to_bigquery_dag/dagRuns'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic your_airflow_basic_auth_credentials'
    }
    data = {'conf': message_data}

    response = requests.post(airflow_endpoint, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f'Error triggering DAG: {response.content}')
