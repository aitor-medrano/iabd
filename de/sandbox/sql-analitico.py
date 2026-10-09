import duckdb

# Conexión en memoria (los datos viven mientras dure el proceso)
con = duckdb.connect()

con.sql("SELECT 'Hola DuckDB desde IABD' AS saludo").show()

SELECT * FROM read_csv_auto('customers.csv') LIMIT 5;

-- O aún más corto: DuckDB infiere el lector por la extensión
SELECT * FROM 'customers.csv' LIMIT 5;

-- Parquet
SELECT count(*) FROM 'orders.parquet';