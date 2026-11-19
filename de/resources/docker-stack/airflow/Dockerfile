# Imagen de Airflow del bloque de Ingeniería de datos.
#
# Airflow no importa dlt ni dbt: los invoca como comandos. Por eso viven en un
# entorno virtual propio (/opt/airflow/elt) y no en el de Airflow. No es una
# preferencia: dbt-core 1.12.3 exige pathspec<1.1 y las constraints de
# Airflow 3.3.2 fijan pathspec==1.1.1, así que no se pueden instalar juntos.
#
# Las versiones llegan como build args desde el .env, las mismas que el nodo lab.

ARG AIRFLOW_IMAGE=apache/airflow:3.4.0
FROM ${AIRFLOW_IMAGE}

ARG DLT_VERSION
ARG DBT_CORE_VERSION
ARG DBT_DUCKDB_VERSION
ARG DUCKDB_VERSION

# PIP_USER=false: la imagen oficial instala por defecto en el directorio del
# usuario airflow, cosa que pip no permite dentro de un entorno virtual.
# SQLAlchemy y PyMySQL: los necesita sql_database de dlt para leer de MySQL.
RUN python -m venv /opt/airflow/elt \
    && PIP_USER=false /opt/airflow/elt/bin/pip install --no-cache-dir \
    "dlt[duckdb,filesystem,s3]==${DLT_VERSION}" \
    "SQLAlchemy>=2.0" \
    "PyMySQL>=1.1" \
    "dbt-core==${DBT_CORE_VERSION}" \
    "dbt-duckdb==${DBT_DUCKDB_VERSION}" \
    "duckdb==${DUCKDB_VERSION}"

# Extensión httpfs (S3/MinIO) instalada en la imagen, como en el nodo lab:
# así las tareas no dependen de descargarla de extensions.duckdb.org.
RUN /opt/airflow/elt/bin/python -c "import duckdb; duckdb.connect().execute('INSTALL httpfs')"

# Los DAG llaman a $ELT_BIN/dbt y $ELT_BIN/python.
ENV ELT_BIN=/opt/airflow/elt/bin