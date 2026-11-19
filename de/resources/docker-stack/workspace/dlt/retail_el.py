import dlt
from dlt.sources.sql_database import sql_database
 
pipeline = dlt.pipeline(
    pipeline_name="retail_el",
    destination=dlt.destinations.duckdb("/workspace/dbt/iabd/retail_el.duckdb"),
    dataset_name="raw",
)
 
fuente = sql_database(credentials="mysql+pymysql://iabd:iabd@mysql-retail:3306/retail_db")
 
pipeline.run(fuente, write_disposition="replace")