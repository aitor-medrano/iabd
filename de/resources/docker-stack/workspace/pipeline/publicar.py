"""Publica los marts de negocio en MinIO como ficheros parquet.
 
Es la última tarea del DAG retail_elt: solo se ejecuta si las pruebas de dbt
han pasado. El cuadro de mandos lee de s3://processed/marts/ y nunca del
fichero DuckDB de trabajo.
"""
import os
 
import duckdb
 
BD = "/workspace/dbt/iabd/retail_el.duckdb"
DESTINO = "s3://processed/marts"
MARTS = ["ingresos_por_departamento", "tasa_devolucion_departamento"]
 
# Solo lectura: publicar no modifica el almacén
con = duckdb.connect(BD, read_only=True)
con.execute("LOAD httpfs")
 
# DuckDB no lee AWS_ENDPOINT_URL: el endpoint de MinIO hay que pasárselo
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
 
for mart in MARTS:
    ruta = f"{DESTINO}/{mart}.parquet"
    con.execute(f"COPY main.{mart} TO '{ruta}' (FORMAT parquet)")
    filas = con.execute(f"SELECT count(*) FROM read_parquet('{ruta}')").fetchone()[0]
    print(f"{mart}: {filas} filas publicadas en {ruta}")