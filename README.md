# superfrete
Data Pipeline com Airflow, GCS, Dataflow e BigQuery
Descrição
Este projeto implementa um pipeline de dados usando o Apache Airflow, integrando serviços do Google Cloud Platform (GCP) como Google Cloud Storage (GCS), Dataflow e BigQuery. O objetivo do pipeline é processar arquivos JSON armazenados no GCS, aplicar transformações usando o Dataflow e carregar os dados processados no BigQuery. Após a carga dos dados, uma verificação de qualidade é realizada para garantir que os dados atendam aos requisitos especificados.

Fluxo do Pipeline
Ingestão:

O pipeline lê arquivos JSON de uma pasta específica no Google Cloud Storage.
Esses arquivos são renovados diariamente e processados em lote.
Processamento (Dataflow):

Um job do Dataflow é disparado pelo Airflow para processar os arquivos JSON.
O Dataflow aplica transformações nos dados conforme o script fornecido.
Carga no BigQuery:

Os dados transformados são carregados no BigQuery em uma tabela designada.
Verificação de Qualidade dos Dados:

Após o carregamento, uma verificação de qualidade dos dados é realizada. O pipeline executa uma consulta SQL no BigQuery para garantir que os dados tenham sido corretamente inseridos e seguem as regras de integridade.
Pré-requisitos
Google Cloud Platform (GCP):

Bucket do GCS: Configure um bucket no GCS para armazenar os arquivos JSON e os resultados do processamento.
BigQuery: Configure um dataset e uma tabela no BigQuery onde os dados processados serão armazenados.
Dataflow: Certifique-se de que o código do job Dataflow (usando Apache Beam ou outro framework compatível) esteja preparado e armazenado em um bucket no GCS.
Apache Airflow:

Airflow deve estar configurado com as permissões adequadas para acessar o GCS, Dataflow e BigQuery.
O pacote do Google Cloud Providers deve estar instalado no Airflow para facilitar a interação com os serviços do GCP:
bash
Copiar código
pip install apache-airflow-providers-google
Python:

Certifique-se de que o job Dataflow foi implementado em Python ou Apache Beam e que está devidamente configurado para ser executado no GCP.
Arquitetura do Pipeline
O fluxo completo do pipeline segue os seguintes passos:

Leitura dos Arquivos JSON no GCS:
O pipeline lê arquivos JSON da pasta json_folder/ dentro do bucket do GCS especificado.
Processamento com Dataflow:
O pipeline dispara um job no Google Dataflow que processa os arquivos JSON e os transforma de acordo com a lógica de negócio.
Carga no BigQuery:
Após o processamento, os dados são carregados na tabela do BigQuery. O operador GCSToBigQueryOperator é utilizado para essa operação.
Verificação de Qualidade dos Dados:
O pipeline executa uma verificação de qualidade no BigQuery, utilizando uma consulta SQL para assegurar que a tabela foi corretamente populada.

Como Executar
Configurar o Airflow:

Garanta que o Google Cloud Connection esteja configurado corretamente no Airflow para autenticação com os serviços GCP.
Configurar o GCS e BigQuery:

Prepare os buckets no GCS e a tabela no BigQuery. Certifique-se de que o bucket de GCS tem os arquivos JSON e de que o Airflow tem permissão de leitura/escrita.
Executar a DAG:

Carregue a DAG no Airflow e inicie a execução manualmente ou espere pela execução agendada diária (@daily).
Verificação de Qualidade dos Dados
Após a carga dos dados no BigQuery, a consulta de verificação de qualidade assegura que a tabela contém registros válidos (com valores não nulos, conforme a lógica de verificação implementada).
É possível adaptar essa verificação conforme as regras de qualidade específicas do negócio.
