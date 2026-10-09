-- Demos del nodo DuckDB.
--   docker compose exec lab duckdb
-- y pega los bloques, o bien:
--   docker compose exec lab duckdb -c ".read /workspace/notebooks/demos.sql"

-- =====================================================================
-- 1. Parquet directo, sin catálogo ni cluster
-- =====================================================================
SELECT count(*) AS pedidos
FROM read_parquet('/sample-data/retail_db/orders/orders.parquet');

-- Join entre dos parquet: ningún servicio de por medio
SELECT c.customer_city AS ciudad,
       count(*)        AS pedidos,
       round(sum(o.order_total), 2) AS importe
FROM read_parquet('/sample-data/retail_db/orders/orders.parquet') o
JOIN read_parquet('/sample-data/retail_db/customers/customers.parquet') c
  ON c.customer_id = o.order_customer_id
WHERE o.order_status = 'COMPLETE'
GROUP BY ciudad
ORDER BY importe DESC;

-- =====================================================================
-- 2. Consultar MySQL directamente (extensión mysql)
--    Contraste con dlt: aquí NO se copia el dato, se consulta en origen.
-- =====================================================================
ATTACH 'host=mysql user=root password=rootpass database=retail_db'
  AS retail (TYPE mysql);

SELECT order_status, count(*) AS n
FROM retail.orders
GROUP BY order_status
ORDER BY n DESC;

-- Federación: MySQL y parquet en la MISMA consulta
SELECT c.customer_city AS ciudad, count(*) AS pedidos
FROM retail.orders o
JOIN read_parquet('/sample-data/retail_db/customers/customers.parquet') c
  ON c.customer_id = o.order_customer_id
GROUP BY ciudad
ORDER BY pedidos DESC;

DETACH retail;

-- =====================================================================
-- 3. Leer HDFS vía WebHDFS (httpfs)
--    DuckDB NO habla el protocolo nativo de HDFS, pero HDFS expone una
--    API REST. Requiere haber ejecutado antes ./scripts/load-sample-data.sh
--    NOTA: pendiente de comprobar en tu equipo; ver README.
-- =====================================================================
-- SELECT count(*)
-- FROM read_parquet(
--   'http://namenode:9870/webhdfs/v1/data/retail_db/orders/orders.parquet?op=OPEN'
-- );

-- =====================================================================
-- 4. Escribir parquet particionado (para subirlo luego a HDFS)
-- =====================================================================
COPY (
  SELECT *, year(cast(order_date AS DATE)) AS anyo
  FROM read_parquet('/sample-data/retail_db/orders/orders.parquet')
) TO '/workspace/data/orders_particionado'
  (FORMAT parquet, PARTITION_BY (anyo), OVERWRITE_OR_IGNORE);
