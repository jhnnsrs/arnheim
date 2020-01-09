from kafka import KafkaConsumer, KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers=['kafka:9092'])

try:
    print('Welcome to parse engine')
    consumer = KafkaConsumer('test', bootstrap_servers='kafka:9092')
    for message in consumer:
        print("hallo")
        future = producer.send('web', b"hallo")
except Exception as e:
    print(e)
    # Logs the error appropriately.
    pass
