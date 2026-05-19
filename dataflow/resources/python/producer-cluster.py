from confluent_kafka import Producer
from json import dumps
import time

producer = Producer({
    'bootstrap.servers': 'localhost:9094,localhost:9095,localhost:9096'
})

for i in range(10):
    producer.produce("iabd-topic-3p2r", value=dumps({"nombre": "producer " + str(i)}).encode('utf-8'))

# Esperamos a que se entreguen todos los mensajes pendientes.
producer.flush()
time.sleep(1)