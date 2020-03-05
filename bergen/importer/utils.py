import os
import shutil
from datetime import datetime

from channels.db import database_sync_to_async

from bioconverter.models import Locker, BioImage
from importer.models import Importing
from larvik.logging import get_module_logger
# Get an instance of a logger
from larvik.structures import LarvikStatus
from django.conf import settings

logger = get_module_logger(__name__)
BIOIMAGE_ROOT = settings.BIOIMAGE_ROOT

@database_sync_to_async
def get_importing_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    logger.info("Getting request of Id {0}".format(request["id"]))
    parsing = Importing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Importing {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def update_status_on_request(parsing: Importing, status: LarvikStatus):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    parsing.statuscode = status.statuscode
    parsing.statusmessage = status.message
    parsing.save()
    return parsing

@database_sync_to_async
def update_importing_with_new_Locker(importing: Importing):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    if importing is None:
        raise ClientError("===")

    locker = Locker.objects.create(creator=importing.creator,
                          name= "Auto Import {0}".format(datetime.now().strftime("%x")),
                          location="None"
                          )
    importing.locker = locker
    importing.save()

    return importing



@database_sync_to_async
def create_bioimages_from_list(filelist, request: Importing, settings):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # %%
    def moveFileToLocker(path,name):

        if os.path.exists(path):
            logger.info("Moving file from " + path)

            directory = "{0}/{1}/".format(request.creator.id, request.locker.id)
            directory = os.path.join(BIOIMAGE_ROOT, directory)

            if not os.path.exists(directory):
                os.makedirs(directory)

            new_path = os.path.join(directory, os.path.basename(name))
            shutil.move(path, new_path)

            logger.info("To New Path of " + new_path)
            name = name if name else os.path.basename(path)
            image = BioImage.objects.create(file=new_path,
                                            creator=request.creator,
                                            locker=request.locker,
                                            name=os.path.basename(name))

            image.save()
            return image

    bioimages = []

    for file in filelist:
        path = file[1]
        name = file[0]
        bioimages.append((moveFileToLocker(path, name),"create"))


    return bioimages



class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code