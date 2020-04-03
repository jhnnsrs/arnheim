import logging

from channels.worker import Worker
from django.core.management import BaseCommand

from larvik.discover import autodiscover, setDiscover

logger = logging.getLogger("django.channels.worker")


class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)


    def handle(self, *args, **options):
        # Get the backend to use
        setDiscover(True)
        autodiscover()
        logger.info("DONE - Restart")