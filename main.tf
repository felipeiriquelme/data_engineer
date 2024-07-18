# main.tf

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 3.0.0"
    }
  }
}

provider "google" {
  credentials = file("/Users/friquelmees/Downloads/womproject-cc761ac3c46f.json")
  project     = "womproject"  # Reemplazar con el ID de tu proyecto
  region      = "us-central1"
}

# Habilitar servicios requeridos
resource "google_project_service" "cloudfunctions" {
  project = "womproject"
  service = "cloudfunctions.googleapis.com"
}

resource "google_project_service" "composer" {
  project = "womproject"
  service = "composer.googleapis.com"
}

# Bucket de Google Cloud Storage para la función
resource "google_storage_bucket" "wom_bucket2" {
  name     = "wom_bucket2"
  location = "us-central1"
}

# Subir el archivo ZIP de la función a Cloud Storage
resource "google_storage_bucket_object" "function_source_zip" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.wom_bucket2.name
  source = "/Users/friquelmees/Downloads/Programas/dataengineer/mi-funcion/function-source.zip"  # Ruta local al archivo ZIP de la función
}

# Cloud Function para activar el DAG en Cloud Composer
resource "google_cloudfunctions_function" "wom_cloud_function" {
  name        = "wom-cloud-function"
  runtime     = "python39"
  entry_point = "trigger_dag"
  source_archive_bucket = google_storage_bucket.wom_bucket2.name
  source_archive_object = google_storage_bucket_object.function_source_zip.name
  trigger_http = true

  environment_variables = {
    DAG_NAME           = "wom-dag"
    AIRFLOW_WEB_URL    = "http://airflow-webserver-service:8080"
    AIRFLOW_API_PATH   = "api/v1/dags/wom-dag/dagRuns"
  }

  depends_on = [
    google_storage_bucket_object.function_source_zip,
  ]
}



# Asignar roles necesarios para Cloud Composer
resource "google_project_iam_member" "composer_roles" {
  project = "womproject"
  role    = "roles/composer.serviceAgent"
  member  = "serviceAccount:service-1087116115357@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "composer_v2_ext_roles" {
  project = "womproject"
  role    = "roles/composer.ServiceAgentV2Ext"
  member  = "serviceAccount:service-1087116115357@cloudcomposer-accounts.iam.gserviceaccount.com"
}


# DAG en Cloud Composer para cargar datos a BigQuery
resource "google_composer_environment" "wom_composer" {
  name   = "wom-composer"
  region = "us-central1"
}
