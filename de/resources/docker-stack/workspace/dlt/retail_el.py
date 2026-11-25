import dlt, os
from dlt.sources.sql_database import sql_database

# La conexión sale de las variables de entorno que define el compose, tanto en lab como en Airflow
credenciales = (
    f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}"
    f"@{os.environ['MYSQL_HOST']}:3306/{os.environ['MYSQL_DATABASE_SOURCE']}"
)

pipeline = dlt.pipeline(
    pipeline_name="retail_el",
    destination=dlt.destinations.duckdb("/workspace/dbt/iabd/retail_el.duckdb"),
    dataset_name="raw",
)

fuente = sql_database(credentials=credenciales)

pipeline.run(fuente, write_disposition="replace")
