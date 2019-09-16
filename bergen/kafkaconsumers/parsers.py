from channels.consumer import AsyncConsumer
from kafka import KafkaProducer
import json

from logpipe import Producer

from metamorphers.serializers import KafkaingSerializer


class ChannelKafkaProducer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.producer = Producer('kafkaing', KafkaingSerializer)
        self.job = None
        self.data = None

    async def send(self,data):
        self.producer.send(data)






class Parsing(ChannelKafkaProducer):

    async def startconverting(self, data):
        await self.send(data)