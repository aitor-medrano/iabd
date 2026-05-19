from confluent_kafka import Consumer, KafkaError
from datetime import datetime
import boto3

BOOTSTRAP_SERVERS = "localhost:9094"

consumer = Consumer({
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "group.id": "iabd-caso3-bronze",      # grupo propio para este consumidor
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
})
consumer.subscribe(["iabd-aemet-bronze"])

# === Conexión con S3 / MinIO ===
# Versión Docker (MinIO):
s3r = boto3.resource(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)
bucket = s3r.Bucket("raw-data")

# Versión Máquina virtual (S3 real):
# s3r = boto3.resource("s3", region_name="us-east-1")
# bucket = s3r.Bucket("iabd-nifi")

try:
    while True:
        m = consumer.poll(1.0)
        if m is None:
            continue
        if m.error():
            if m.error().code() == KafkaError._PARTITION_EOF:
                continue
            print(f"Error: {m.error()}")
            continue

        # Guardamos el JSON tal cual, dentro de la carpeta bronze/
        nom_fichero = "bronze/" + datetime.now().isoformat() + ".json"
        bucket.put_object(Key=nom_fichero, Body=m.value())
        print(f"Guardado {nom_fichero} (P:{m.partition()} O:{m.offset()})")
finally:
    consumer.close()