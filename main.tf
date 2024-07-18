resource "google_bigquery_dataset" "bd_tf" {

   dataset_id = "wom"

}

resource "google_bigquery_table" "table_tf" {

   table_id = "wom1"
   dataset_id = google_bigquery_dataset.bd_tf.dataset_id
}
