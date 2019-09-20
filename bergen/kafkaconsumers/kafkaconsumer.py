from channels.consumer import AsyncConsumer
from kafka import KafkaConsumer


class ChannelKafkaConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.consumer = KafkaConsumer('web',bootstrap_servers=['kafka:9092'])
        self.startListening()

    def startListening(self):
        print("LOADED")
        for message in self.consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))

            path = "nan"
            stream = "noino"
            method = "lala"
            serializer = {}
            serializer.data = 0
            self.channel_layer.group_send(
                path,
                {
                    "type": "stream",
                    "stream": stream,
                    "room": path,
                    "method": method,
                    "data": serializer.data
                }
            )







# To consume latest messages and auto-commit offsets


