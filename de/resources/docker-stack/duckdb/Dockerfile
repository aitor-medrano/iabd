# Nodo de ingeniería de datos: DuckDB (CLI + Python) + dlt + dbt + JupyterLab.
# A diferencia de Hadoop/Hive, esta imagen es multi-arch: en Apple Silicon
# se construye y ejecuta como arm64 NATIVO (sin emulación).
FROM python:3.12-slim

ARG DUCKDB_VERSION=1.5.4
ARG MC_VERSION=RELEASE.2025-08-13T08-35-41Z

# TARGETARCH lo inyecta BuildKit automáticamente: amd64 | arm64.
# Los assets del release de DuckDB usan exactamente esos nombres.
ARG TARGETARCH

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl unzip ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

# CLI de DuckDB (para las sesiones de SQL puro: duckdb -c "...")
RUN curl -fsSL -o /tmp/duckdb.zip \
      "https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-${TARGETARCH}.zip" \
    && unzip -q /tmp/duckdb.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/duckdb \
    && rm /tmp/duckdb.zip \
    && duckdb -c "SELECT version() AS duckdb_cli;"

# MinIO Client
RUN curl -fsSL \
    "https://github.com/minio/mc/releases/download/${MC_VERSION}/mc.linux-${TARGETARCH}.${MC_VERSION}" \
    -o /usr/local/bin/mc; \
    chmod +x /usr/local/bin/mc; \
    mc --version

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Extensiones preinstaladas EN LA IMAGEN.
# DuckDB las descarga bajo demanda la primera vez que se usan; si la red del
# aula las bloquea (o no hay internet), `dbt run` falla nada más arrancar
# porque profiles.yml declara httpfs. Horneándolas aquí, el aula no depende
# de extensions.duckdb.org.
#   httpfs  -> S3/MinIO y HTTP (incluido WebHDFS)
#   mysql   -> ATTACH directo contra retail_db
RUN duckdb -c "INSTALL httpfs; INSTALL mysql; INSTALL parquet;" \
 && python -c "import duckdb; c=duckdb.connect(); [c.execute('INSTALL '+e) for e in ('httpfs','mysql','parquet')]" \
 && duckdb -c "SELECT extension_name, installed FROM duckdb_extensions() WHERE installed;"

# dbt busca los perfiles en DBT_PROFILES_DIR
ENV DBT_PROFILES_DIR=/workspace/dbt/iabd
# Evita que dbt envíe telemetría desde los equipos del aula
ENV DO_NOT_TRACK=1

WORKDIR /workspace
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", \
     "--allow-root", "--ServerApp.token=", "--ServerApp.password=", \
     "--ServerApp.root_dir=/workspace"]
