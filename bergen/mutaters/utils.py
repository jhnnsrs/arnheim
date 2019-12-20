import io

from channels.db import database_sync_to_async
from django.core.files.uploadedfile import InMemoryUploadedFile

from larvik.consumers import LarvikError
from mutaters.models import Mutating, Reflection


@database_sync_to_async
def get_mutating_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Mutating.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Mutating {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def reflection_update_or_create(image, request: Mutating, settings) -> [(Reflection, str)]:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    reflection: Reflection = Reflection.objects.filter(transformation=request.transformation).filter(nodeid=request.nodeid).first()
    method = "update"
    if reflection is None:
        #TODO make creation of outputvid
        reflection = Reflection.objects.create(transformation=request.transformation, creator=request.creator, nodeid=request.nodeid, roi=request.transformation.roi,
                                                  sample=request.sample, shape=request.transformation.shape, experiment=request.transformation.experiment)
        method = "create"
    if reflection is not None:
        #TODO: update array of output
        path = "sample-{0}_transformation-{1}_node-{2}".format(str(reflection.sample.id), str(reflection.transformation.id), str(request.nodeid))
        img_io = io.BytesIO()
        image.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        reflection.image = thumb_file
        reflection.save()
        print("YES")
    else:
        raise LarvikError("FATAL ERROR SOMEWHERE")
    return [(reflection, method)]

@database_sync_to_async
def update_image_on_reflection(request: Mutating, image) -> (Reflection, str):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    reflection: Reflection = Reflection.objects.filter(transformation=request.transformation).filter(nodeid=request.nodeid).first()
    method = "update"
    if reflection is None:
        #TODO make creation of outputvid
        reflection = Reflection.objects.create(transformation=request.transformation, creator=request.creator, nodeid=request.nodeid, roi=request.transformation.roi,
                                                  sample=request.sample, shape=request.transformation.shape, experiment=request.transformation.experiment)
        method = "create"
    if reflection is not None:
        #TODO: update array of output
        path = "sample-{0}_transformation-{1}_node-{2}".format(str(reflection.sample.id), str(reflection.transformation.id), str(request.nodeid))
        img_io = io.BytesIO()
        image.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        reflection.image = thumb_file
        reflection.save()
        print("YES")
    else:
        print("FATAL ERROR SOMEWHERE")
    return reflection, method

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code