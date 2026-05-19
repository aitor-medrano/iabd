from confluent_kafka import Consumer, Producer, KafkaError
from datetime import datetime
from json import loads, dumps
from pymongo import MongoClient
import boto3
import pandas as pd

# === Configuración (ajustar según entorno) ===
BOOTSTRAP_SERVERS = "localhost:9094"
MONGO_URI         = "mongodb+srv://iabd:iabdiabd@cluster0.4hm7u8y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
S3_ENDPOINT       = "http://localhost:9000"
S3_KEY            = "minioadmin"
S3_SECRET         = "minioadmin123"
S3_BUCKET         = "raw-data"

# Convierte un diccionario JSON con todo el contenido en String a diferentes
# tipos (float, datetime, ...) usando object_hook al hacer json.loads()
def esquema_json(dct):
    result = {}
    if "fecha" in dct:
        result["fecha"] = datetime.fromisoformat(dct["fecha"])
    if "temp" in dct:
        result["temp"] = float(dct["temp"])
    if "humedad" in dct:
        result["humedad"] = float(dct["humedad"])
    if "ciudad" in dct:
        result["ciudad"] = dct["ciudad"]
    return result

# Paso 1 - Consumir Silver
consumer = Consumer({
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "group.id": "iabd-caso3-silver",     # grupo propio, distinto del bronze
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
})
consumer.subscribe(["iabd-aemet-silver"])

# Paso 2 - Conexión con S3 / MinIO
# (Versión Docker; en la VM basta con boto3.resource("s3", region_name="us-east-1"))
s3r = boto3.resource(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
    region_name="us-east-1",
)
bucket = s3r.Bucket(S3_BUCKET)

# Paso 3 - Conexión con MongoDB
clienteMongo = MongoClient(MONGO_URI)
colcaso3 = clienteMongo.iabd.caso3

# Paso 5 - Producir Gold
producer = Producer({
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "client.id": "productor-gold",
    "acks": "all",
    "enable.idempotence": True,
})

def delivery_report(err, msg):
    if err is not None:
        print(f"Error entregando a {msg.topic()}: {err}")
    else:
        print(f"Mensaje gold enviado [P:{msg.partition()} O:{msg.offset()}]")

mensajes = []

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

        valor_bytes = m.value()
        doc_json = loads(valor_bytes.decode("utf-8"), object_hook=esquema_json)
        mensajes.append(doc_json)

        # Paso 2 - Guardamos el mensaje en S3/MinIO
        nom_fichero = "silver/" + datetime.now().isoformat() + ".json"
        bucket.put_object(Key=nom_fichero, Body=valor_bytes)

        # Paso 3 - Lo insertamos en MongoDB
        # Importante: insert_one() añade el campo _id al dict; para no
        # contaminar la lista que usaremos en el agregado, pasamos una copia.
        colcaso3.insert_one(doc_json.copy())

        # Paso 4 - Cada 10 mensajes calculamos el agregado
        if len(mensajes) == 10:
            pd_mensajes = pd.DataFrame(mensajes)
            pd_agg = (
                pd_mensajes
                .groupby("ciudad")
                .agg(fecha=("fecha", "max"),
                     temp=("temp", "mean"),
                     humedad=("humedad", "mean"))
                .reset_index()
            )

            # Convertimos a list[dict] y dejamos las fechas como ISO para
            # serializar una sola vez.
            registros = pd_agg.to_dict(orient="records")
            for r in registros:
                if hasattr(r["fecha"], "isoformat"):
                    r["fecha"] = r["fecha"].isoformat()

            mensaje_gold = dumps(registros).encode("utf-8")
            print(f"Mensaje gold: {mensaje_gold.decode('utf-8')}")

            # Paso 5 - Lo producimos al topic gold
            producer.produce(
                "iabd-aemet-gold",
                value=mensaje_gold,
                callback=delivery_report,
            )
            producer.poll(0)

            # Vaciamos el buffer para el siguiente bloque de 10
            mensajes = []
finally:
    print("Cerrando consumidor y productor...")
    producer.flush(timeout=10)
    consumer.close()
    clienteMongo.close()