from time import sleep

from kafka import KafkaConsumer, KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))

print("Doing its dead")
for e in range(1000):
    data = {'number' : e}
    producer.send('test', value=data)

    print("Sending")
    sleep(2)