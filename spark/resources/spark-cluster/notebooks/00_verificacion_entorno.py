# %% [markdown]
# # Spark 4 Cluster - Notebook de verificacion
# Comprueba la conexion con todos los servicios: Spark 4, Hive/MySQL, MinIO (S3) y Kafka.
# Incluye ejemplos de novedades de Spark 4: VARIANT, SQL UDFs, pipe syntax.

# %% [markdown]
# ## 1. Crear SparkSession con Hive + S3 + Kafka

# %%
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("spark://spark-master:7077")
    .appName("spark4-full-stack-demo")
    # --- Hive ---
    .config("spark.sql.catalogImplementation", "hive")
    .config("spark.sql.warehouse.dir", "s3a://warehouse/hive")
    # --- Classpath (JDBC + Hadoop-AWS + Kafka) ---
    .config("spark.driver.extraClassPath", "/usr/local/spark/extra-jars/*")
    .config("spark.executor.extraClassPath", "/opt/bitnami/spark/extra-jars/*")
    # --- MinIO / S3A ---
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
    # --- Paquetes (Scala 2.13 para Spark 4) ---
    .config("spark.jars.packages", ",".join([
        "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0",
        "org.apache.hadoop:hadoop-aws:3.4.1",
        "com.amazonaws:aws-java-sdk-bundle:1.12.367",
    ]))
    # --- ANSI mode (por defecto en Spark 4) ---
    .config("spark.sql.ansi.enabled", "true")
    .enableHiveSupport()
    .getOrCreate()
)

print(f"Spark version: {spark.version}")
print(f"Spark UI (driver): http://localhost:4040")
print(f"Spark Master UI:   http://localhost:8080")

# %% [markdown]
# ## 2. Hive + MySQL Metastore

# %%
spark.sql("CREATE DATABASE IF NOT EXISTS demo")
spark.sql("USE demo")

spark.sql("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INT,
        producto STRING,
        cantidad INT,
        precio DOUBLE,
        fecha DATE
    )
    COMMENT 'Tabla de ejemplo de ventas'
""")

spark.sql("""
    INSERT INTO ventas VALUES
    (1, 'Laptop',   5,  999.99, DATE '2025-01-15'),
    (2, 'Mouse',    50, 19.99,  DATE '2025-01-16'),
    (3, 'Teclado',  30, 49.99,  DATE '2025-01-17'),
    (4, 'Monitor',  10, 349.99, DATE '2025-02-01'),
    (5, 'Webcam',   20, 79.99,  DATE '2025-02-05')
""")

spark.sql("SELECT * FROM ventas ORDER BY fecha").show()
spark.sql("SHOW TABLES IN demo").show()

# %% [markdown]
# ## 3. MinIO (S3) - Leer y escribir Parquet

# %%
df = spark.sql("SELECT * FROM demo.ventas")
df.write.mode("overwrite").parquet("s3a://processed/ventas_parquet")

df_s3 = spark.read.parquet("s3a://processed/ventas_parquet")
df_s3.show()
print(f"Registros leidos desde MinIO: {df_s3.count()}")

# %% [markdown]
# ## 4. Kafka - Producir y consumir mensajes

# %%
from pyspark.sql.functions import to_json, struct, col

df_kafka = (
    spark.sql("SELECT * FROM demo.ventas")
    .select(
        col("id").cast("string").alias("key"),
        to_json(struct("*")).alias("value")
    )
)

(
    df_kafka.write
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("topic", "ventas-eventos")
    .save()
)

print("Mensajes enviados a Kafka topic 'ventas-eventos'")

# %%
# Leer desde Kafka (batch)
df_from_kafka = (
    spark.read
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "ventas-eventos")
    .option("startingOffsets", "earliest")
    .load()
)

df_from_kafka.selectExpr(
    "CAST(key AS STRING)",
    "CAST(value AS STRING)",
    "topic",
    "partition",
    "offset",
    "timestamp"
).show(truncate=False)

# %% [markdown]
# ## 5. Novedades de Spark 4
#
# ### 5a. Tipo VARIANT (datos semi-estructurados)

# %%
# VARIANT permite almacenar JSON semi-estructurado de forma nativa
spark.sql("""
    SELECT
        parse_json('{"nombre": "Ana", "edad": 30, "tags": ["vip", "premium"]}') AS datos,
        parse_json('{"nombre": "Luis", "edad": 25}') AS datos2
""").show(truncate=False)

# Extraer campos de VARIANT
spark.sql("""
    WITH raw AS (
        SELECT parse_json('{"producto": "Laptop", "specs": {"ram": 16, "cpu": "i7"}}') AS v
    )
    SELECT
        v:producto AS producto,
        v:specs.ram AS ram,
        v:specs.cpu AS cpu
    FROM raw
""").show()

# %% [markdown]
# ### 5b. SQL User-Defined Functions (SQL UDFs)

# %%
# Spark 4 permite crear UDFs directamente en SQL (sin Python/Scala)
spark.sql("""
    CREATE OR REPLACE TEMPORARY FUNCTION calcular_iva(precio DOUBLE)
    RETURNS DOUBLE
    RETURN precio * 1.21
""")

spark.sql("""
    SELECT producto, precio, calcular_iva(precio) AS precio_con_iva
    FROM demo.ventas
""").show()

# %% [markdown]
# ### 5c. Pipe Syntax (operador |>)

# %%
# El pipe syntax permite encadenar transformaciones de forma mas legible
spark.sql("""
    SELECT * FROM demo.ventas
    |> WHERE cantidad > 10
    |> SELECT producto, cantidad, precio * cantidad AS total
    |> ORDER BY total DESC
""").show()

# %% [markdown]
# ### 5d. ANSI Mode por defecto
# En Spark 4, `spark.sql.ansi.enabled` es `true` por defecto.
# Esto significa que operaciones invalidas lanzan errores en vez de devolver NULL.

# %%
# Esto lanza un error en Spark 4 (en Spark 3 devolveria NULL)
try:
    spark.sql("SELECT CAST('abc' AS INT)").show()
except Exception as e:
    print(f"Error esperado (ANSI mode): {e}")

# %% [markdown]
# ## 6. Structured Streaming desde Kafka (opcional)
# Descomenta para probar streaming en tiempo real.

# %%
# streaming_df = (
#     spark.readStream
#     .format("kafka")
#     .option("kafka.bootstrap.servers", "kafka:9092")
#     .option("subscribe", "ventas-eventos")
#     .option("startingOffsets", "latest")
#     .load()
#     .selectExpr("CAST(value AS STRING) as json_value")
# )
#
# query = (
#     streaming_df.writeStream
#     .format("console")
#     .outputMode("append")
#     .option("truncate", False)
#     .start()
# )
#
# import time
# time.sleep(30)
# query.stop()

# %% [markdown]
# ## 7. Resumen del entorno

# %%
print("=" * 60)
print(" RESUMEN DEL ENTORNO - SPARK 4")
print("=" * 60)
print(f" Spark Master UI:   http://localhost:8080")
print(f" Spark Driver UI:   http://localhost:4040")
print(f" Jupyter Lab:       http://localhost:8888 (token: spark)")
print(f" MinIO Console:     http://localhost:9001 (minioadmin / minioadmin123)")
print(f" Kafka UI:          http://localhost:8081")
print(f" MySQL:             localhost:3306 (hive / hivepass)")
print(f"")
print(f" Spark version:     {spark.version}")
print(f" ANSI mode:         {spark.conf.get('spark.sql.ansi.enabled')}")
print(f" Workers activos:   {spark.sparkContext.defaultParallelism}")
print("=" * 60)
