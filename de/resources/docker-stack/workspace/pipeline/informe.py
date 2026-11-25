"""Informe de ingresos por departamento a partir de los marts publicados en MinIO."""
import os
 
import duckdb
 
ORIGEN = "s3://processed/marts/ingresos_por_departamento.parquet"
 
con = duckdb.connect()
con.execute("LOAD httpfs")
endpoint = os.environ["AWS_ENDPOINT_URL"].removeprefix("http://")
con.execute(f"""
    CREATE SECRET minio (
        TYPE s3,
        KEY_ID '{os.environ["AWS_ACCESS_KEY_ID"]}',
        SECRET '{os.environ["AWS_SECRET_ACCESS_KEY"]}',
        ENDPOINT '{endpoint}',
        URL_STYLE 'path',
        USE_SSL false
    )
""")
 
con.sql(f"SELECT * FROM read_parquet('{ORIGEN}') ORDER BY ingresos DESC").show()