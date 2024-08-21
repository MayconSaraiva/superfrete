from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowCreateJobOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator

# Padrões para Daag
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

# Definições da DAG
dag = DAG(
    'gcs_to_bigquery',
    default_args=default_args,
    description='Processa arquivos JSON que estão no GCS utilizando o Dataflow para carregar no BigQuery',
    schedule_interval='@daily', # Diario, Horario, Schedule de acordo com a necessidade.
)

start_pipeline = DummyOperator(
    task_id='start_pipeline',
    dag=dag,
)

end_pipeline = DummyOperator(
    task_id='end_pipeline',
    dag=dag,
)

# Move e Verifica os Arquivos JSON no GCS
move_files_gcs = GCSToGCSOperator(
    task_id='move_files_gcs',
    source_bucket='gs-superfrete',  # Bucket onde os arquivos estão
    source_object='json_arquivos/*.json',  # Todos os JSONs na pasta especificada
    destination_bucket='bkp',  # Bucket destino, se precisar mover para bkp
    destination_object='processed/',  # Pasta de destino após processamento
    move_object=True,  
    dag=dag,
)

# Aciona o Dataflow para o processo de carga
start_dataflow_job = DataflowCreateJobOperator(
    task_id="start_dataflow_job",
    job_name="dataflow-json-processing",
    py_file="gs://gs-superfrete/path-to-your-dataflow-job.py",  # Caminho para o script Python do job Dataflow
    options={
        'input': 'gs://source_bucket_name/json_arquivos/*.json',  # Arquivos de entrada
        'output': 'gs://destination_bucket_name/processed/',  # Saída processada
        'temp_location': 'gs://gs-superfrete/temp',  # Local temporário
        'runner': 'DataflowRunner',
        'project': 'your-gcp-project',
        'region': 'us-central1',
    },
    location='us-central1',
    dag=dag,
)

# Carrega os dados no Big Query
load_to_bigquery = GCSToBigQueryOperator(
    task_id='load_to_bigquery',
    bucket='destination_bucket_name',
    source_objects=['processed/*.json'],  # Dados processados pela Dataflow
    destination_project_dataset_table='your_project.your_dataset.your_table',
    source_format='NEWLINE_DELIMITED_JSON',
    write_disposition='WRITE_APPEND',
    autodetect=True,  
    dag=dag,
)

# Data Quality
data_quality_check = BigQueryInsertJobOperator(
    task_id='data_quality_check',
    configuration={
        "query": {
            "query": """
            SELECT COUNT(*) FROM `your_project.your_dataset.your_table` 
            WHERE column_name IS NOT NULL
            """,  
            "useLegacySql": False,
        }
    },
    location='US',
    dag=dag,
)

# Orquestrando as tarefas
start_pipeline >> move_files_gcs >> start_dataflow_job >> load_to_bigquery >> data_quality_check >> end_pipeline
