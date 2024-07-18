# main.py

import requests
import os

def trigger_dag(request):
    # Nombre del DAG que quieres activar
    dag_name = os.getenv('DAG_NAME', 'wom-dag')

    # URL de Airflow Webserver
    airflow_web_url = os.getenv('AIRFLOW_WEB_URL', 'http://airflow-webserver-service:8080')

    # Ruta de la API para activar DAGs en Airflow
    airflow_api_path = os.getenv('AIRFLOW_API_PATH', 'api/v1/dags/{}/dagRuns'.format(dag_name))

    # URL completa para activar el DAG
    trigger_url = '{}{}'.format(airflow_web_url, airflow_api_path)

    # Payload para activar el DAG (puede estar vacío dependiendo de tu configuración)
    payload = {}

    # Realizar la solicitud POST para activar el DAG
    response = requests.post(trigger_url, json=payload)

    if response.status_code == 200:
        return 'DAG {} triggered successfully'.format(dag_name)
    else:
        return 'Failed to trigger DAG {}: {}'.format(dag_name, response.text)
