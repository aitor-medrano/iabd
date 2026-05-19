from confluent_kafka import Consumer
from json import loads

consumer = Consumer({
    'bootstrap.servers': 'localhost:9094,localhost:9095,localhost:9096',
    'group.id': 'iabd-grupo-1',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
})
consumer.subscribe(['iabd-topic-3p2r'])

try:
    while True:
        m = consumer.poll(1.0)
        if m is None:
            continue
        if m.error():
            print(f"Error: {m.error()}")
            continue

        value = loads(m.value().decode('utf-8'))
        print(f"P:{m.partition()} O:{m.offset()} K:{m.key()} V:{value}")
finally:
    consumer.close()