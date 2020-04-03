import json
import traceback
from typing import Callable
from uuid import UUID

from channels.db import database_sync_to_async
from dask.callbacks import Callback
from distributed import WorkerPlugin

from larvik.structures import LarvikStatus


class TemporaryFile(object):
    def __init__(self, field, tmp="/tmp"):
        self.field = field
        self.tmppath = tmp

    def __enter__(self):
        import os
        import uuid
        _, file_extension = os.path.splitext(self.field.name)
        self.filename = self.tmppath + "/" + str(uuid.uuid4()) + file_extension
        with open(self.filename, 'wb+') as destination:
            for chunk in self.field.chunks():
                destination.write(chunk)

        return self.filename

    def __exit__(self, exc_type, exc_value, tb):
        import os
        os.remove(self.filename)
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            # return False # uncomment to pass exception through

        return True


@database_sync_to_async
def update_status_on_larvikjob(parsing, status: LarvikStatus):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing.statuscode = status.statuscode
    parsing.statusmessage = status.message
    parsing.save()
    return parsing


# This is necessary so that we serialize the uuid correctly
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class DaskRequestUpdater(Callback):

     def __init__(self, start=None, start_state=None, pretask=None, posttask=None, finish=None, callback:Callable[[str, str], None]=None):
          super().__init__(start=start, start_state=start_state, pretask=pretask, posttask=posttask, finish=finish)
          self.callback=callback

     def _pretask(self, key, dask, state):
        """Print the key of every task as it's started"""
        print("Computing: {0}!".format(repr(key)))
        if self.callback is not None: self.callback("start",repr(key))


class TransitionLogger(WorkerPlugin):
    def __init__(self, logger):
        self.logger = logger

        self.logger.info(f'Testing')

    def setup(self, worker):
        self.worker = worker

    def transition(self, key, start, finish, *args, **kwargs):
        self.logger.info(f'{key}')
        if finish == 'error':
            exc = self.worker.exceptions[key]
            self.logger.error("Task '%s' has failed with exception: %s" % (key, str(exc)))