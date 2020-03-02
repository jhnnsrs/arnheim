import io
import os

import nibabel as nib
import numpy as np
from channels.db import database_sync_to_async
from django.core.files.uploadedfile import InMemoryUploadedFile

from elements.models import Representation
from mandal.settings import MEDIA_ROOT, NIFTI_ROOT
from metamorphers.models import Metamorphing, Display, Exhibit


@database_sync_to_async
def get_metamorphing_or_error(request: dict) -> Metamorphing:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = Metamorphing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("ConversionRequest {0} does not exist".format(str(request["id"])))
    return parsing


@database_sync_to_async
def get_inputrepresentation_or_error(request: Metamorphing) -> (Representation, np.array):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    inputrep: Representation = request.representation
    if inputrep.numpy is not None:
        array = inputrep.numpy.get_array()
    else:
        #TODO: This should never be called because every representation should have a nparray on creation
        print("ERROR ON INPUTREPRESENTATION")
        array = np.zeros((1024,1024,3))
    if inputrep is None:
        raise ClientError("Inputvid {0} does not exist on Sample {1}".format(str(request.nodeid), request.sample))
    return inputrep, array

@database_sync_to_async
def exhibit_update_or_create(nifti, request: Metamorphing, settings) -> (Exhibit, str):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    exhibit: Exhibit = Exhibit.objects.filter(representation=request.representation).filter(nodeid=request.nodeid).first()
    method = "update"
    name = "Exhibit of" + request.representation.name
    if exhibit is None:
        #TODO make creation of outputvid
        niftipaths = "sample-{0}_representation-{1}_nodeid-{2}.nii.gz".format(request.sample_id, request.representation_id,request.nodeid)
        niftipath = os.path.join(NIFTI_ROOT, niftipaths)
        nib.save(nifti, niftipath)
        niftiwebpath = os.path.join(os.path.join(MEDIA_ROOT,"/nifti"),niftipaths)

        exhibit = Exhibit.objects.create(representation=request.representation, name=name, creator=request.creator, nodeid=request.nodeid, shape=request.representation.shape,
                                                  sample=request.sample, experiment=request.representation.experiment, niftipath=niftiwebpath)


        print(niftipath)
        exhibit.save()
        method = "create"
    else:
        #TODO: update array of output
        niftipath = "sample-{0}_representation-{1}_node-{2}.nii.gz".format(request.sample_id, request.representation_id,request.nodeid)
        niftiwebpath = os.path.join(os.path.join(MEDIA_ROOT, "/nifti"), niftipath)
        niftilocalpath = os.path.join(NIFTI_ROOT, niftipath)
        nib.save(nifti, niftilocalpath)
        exhibit.niftipath = niftiwebpath
        exhibit.save()
        print("YES")
    return [(exhibit, method)]



@database_sync_to_async
def update_exhibit_or_create(request: Metamorphing, nifti) -> (Exhibit, str):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    exhibit: Exhibit = Exhibit.objects.filter(representation=request.representation).filter(nodeid=request.nodeid).first()
    method = "update"
    name = "Exhibit of" + request.representation.name
    if exhibit is None:
        #TODO make creation of outputvid
        niftipaths = "sample-{0}_representation-{1}_nodeid-{2}.nii.gz".format(request.sample_id, request.representation_id,request.nodeid)
        niftipath = os.path.join(NIFTI_ROOT, niftipaths)
        nib.save(nifti, niftipath)
        niftiwebpath = os.path.join(os.path.join(MEDIA_ROOT,"/nifti"),niftipaths)

        exhibit = Exhibit.objects.create(representation=request.representation, name=name, creator=request.creator, nodeid=request.nodeid, shape=request.representation.shape,
                                                  sample=request.sample, experiment=request.representation.experiment, niftipath=niftiwebpath)


        print(niftipath)
        exhibit.save()
        method = "create"
    else:
        #TODO: update array of output
        niftipath = "sample-{0}_representation-{1}_node-{2}.nii.gz".format(request.sample_id, request.representation_id,request.nodeid)
        niftiwebpath = os.path.join(os.path.join(MEDIA_ROOT, "/nifti"), niftipath)
        niftilocalpath = os.path.join(NIFTI_ROOT, niftipath)
        nib.save(nifti, niftilocalpath)
        exhibit.niftipath = niftiwebpath
        exhibit.save()
        print("YES")
    return exhibit, method

@database_sync_to_async
def update_display_or_create(request: Metamorphing, image) -> (Display, str):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    display: Display = Display.objects.filter(representation=request.representation).filter(nodeid=request.nodeid).first()
    method = "update"
    name = "Display of " + request.representation.name
    if display is None:
        #TODO make creation of outputvid
        display = Display.objects.create(representation=request.representation, name=name, creator=request.creator, nodeid=request.nodeid,
                                                  sample=request.sample, shape=request.representation.shape, experiment=request.representation.experiment)
        method = "create"

    #TODO: update array of output
    path = "sample-{0}_representation-{1}_node-{2}".format(str(display.sample.id), str(display.representation.id), str(request.nodeid))
    img_io = io.BytesIO()
    image.save(img_io, format='jpeg', quality=100)
    thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                      img_io.tell, None)

    display.image = thumb_file
    display.save()
    print("YES")
    return display, method



class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code