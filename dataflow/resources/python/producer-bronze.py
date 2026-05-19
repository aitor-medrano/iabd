from confluent_kafka import Producer
from json import dumps
from datetime import datetime
import time
import requests

# Cambiar según el entorno (ver bloque anterior)
BOOTSTRAP_SERVERS = "localhost:9094"

def delivery_report(err, msg):
    if err is not None:
        print(f"Error entregando mensaje: {err}")
    else:
        print(f"Entregado a {msg.topic()} [P:{msg.partition()} O:{msg.offset()}]")

producer = Producer({
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "client.id": "productor-aemet",
    "acks": "all",                # Esperamos confirmación del líder
    "enable.idempotence": True,   # Evita duplicados ante reintentos
})

url_aemet = "https://api.el-tiempo.net/json/v3/provincias/03/municipios/03065"

while True:
    try:
        r = requests.get(url_aemet, timeout=10)
        r.raise_for_status()
        resp_json = r.json()
    except Exception as e:
        print(f"Error consultando AEMET: {e}")
        time.sleep(10)
        continue

    # 1) Mensaje BRONZE: la respuesta REST tal cual
    producer.produce(
        "iabd-aemet-bronze",
        value=dumps(resp_json).encode("utf-8"),
        callback=delivery_report,
    )

    # 2) Mensaje SILVER: extraemos los campos que nos interesan
    datos_json = {
        "fecha":   datetime.now().isoformat(),
        "ciudad":  resp_json["municipio"]["NOMBRE"],
        "temp":    resp_json["temperatura_actual"],
        "humedad": resp_json["humedad"],
    }
    producer.produce(
        "iabd-aemet-silver",
        value=dumps(datos_json).encode("utf-8"),
        callback=delivery_report,
    )

    # poll(0) procesa los callbacks pendientes sin bloquear
    producer.poll(0)

    time.sleep(60)