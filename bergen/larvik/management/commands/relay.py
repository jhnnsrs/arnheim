from json import loads

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

from mandal import settings

channel_layer = get_channel_layer()


def sse_encode(data):
	out = 'event: message\n'
	for line in data.split('\n'):
		out += 'data: %s\n' % line
	out += '\n'
	return out

class Command(BaseCommand):
	help = 'Relay events from Kafka to GRIP proxy.'

	def handle(self, *args, **options):
		c = KafkaConsumer("test",
						  auto_offset_reset='earliest',
						  enable_auto_commit=True,
						  value_deserializer=lambda x: loads(x.decode('utf-8')),
						  bootstrap_servers="kafka:9092")

		self.stdout.write('subscribed')

		for msg in c:
			print(msg)
			print("Received Message")

			if msg is None:
				continue

			if msg.error():
				if msg.error().code() == KafkaError("Trouble"):
					continue
				else:
					raise Exception("HAHLAHO")

			# skip internal channels
			if msg.topic().startswith('__'):
				continue

			try:
				data = msg.value().decode('utf-8')
			except Exception:
				self.stdout.write('%s: message is not valid utf-8: %s' %
					(msg.topic(), repr(msg.value())))
				continue

			async_to_sync(channel_layer.group_send)(data, {"type": "stream", "stream": "kafka", "room": msg.topic(),
														   "method": "create", "data": data})


		print("Received END")

