"""Ingesta (EL) con dlt: MySQL retail_db -> DuckDB.

dlt se encarga de la extracción, la inferencia de esquema y la carga.
La transformación es cosa de dbt: aquí los datos aterrizan "en crudo"
en el esquema `retail_raw`.

Uso:
    docker compose exec lab python /workspace/dlt/dlt_mysql_to_duckdb.py

Carga incremental:
    Descomenta el bloque `incremental` para que las ejecuciones sucesivas
    sólo traigan los pedidos nuevos en lugar de recargarlo todo.
"""
import dlt
from dlt.sources.sql_database import sql_database

# El servicio se llama "mysql" dentro de la red del compose
CONN = "mysql+pymysql://root:rootpass@mysql:3306/retail_db"

# Fichero DuckDB compartido con dbt (ver profiles.yml)
DB_PATH = "/workspace/data/retail.duckdb"


def main():
    source = sql_database(
        credentials=CONN,
        table_names=["customers", "orders"],
    )

    # --- Carga incremental (opcional) --------------------------------
    # source.orders.apply_hints(
    #     incremental=dlt.sources.incremental("order_date")
    # )
    # -----------------------------------------------------------------

    pipeline = dlt.pipeline(
        pipeline_name="retail",
        destination=dlt.destinations.duckdb(DB_PATH),
        dataset_name="retail_raw",
    )

    info = pipeline.run(source, write_disposition="replace")
    print(info)

    # Comprobación rápida de lo cargado
    with pipeline.sql_client() as client:
        for tabla in ("customers", "orders"):
            with client.execute_query(f"SELECT count(*) FROM {tabla}") as cur:
                print(f"retail_raw.{tabla}: {cur.fetchone()[0]} filas")


if __name__ == "__main__":
    main()
