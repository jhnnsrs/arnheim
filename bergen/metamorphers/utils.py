import io
import os

import nibabel as nib
import numpy as np
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from bioconverter.models import ConversionRequest
from filterbank.models import Parsing, Representation, AImage, Nifti
from metamorphers.models import Metamorphing, Display, Exhibit
from multichat.settings import MEDIA_ROOT, NIFTI_ROOT


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
def update_outputrepresentation_or_create(request: ConversionRequest, numpyarray):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.outputvid).first()
    if outputrep is None:
        method = "create"
        #TODO make creation of outputvid
        outputrep = Representation.objects.create(name="Initial Stack",creator=request.creator,vid=request.outputvid,sample=request.sample,experiment=request.experiment,numpy=numpyarray)
    elif outputrep is not None:
        #TODO: update array of output
        method = "update"
        outputrep.nparray.set_array(numpyarray)
    return outputrep, method


@database_sync_to_async
def get_inputmodel_or_error(model,pk) -> models.Model:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    print(pk)
    print(model)
    inputmodel = model.objects.get(pk=pk)
    if inputmodel is None:
        raise ClientError("Inputmodel {0} does not exist".format(str(pk)))
    return inputmodel




@database_sync_to_async
def update_image_on_outputrepresentation_or_error(request: ConversionRequest, original_image, path) -> Representation:
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.outputvid).first()
    if outputrep is None:
        #TODO make creation of outputvid
        raise ClientError("VID {0} does nots exist on Sample {1}".format(str(request.outputvid), request.sample))
    elif outputrep is not None:
        #TODO: update array of output
        img_io = io.BytesIO()
        original_image.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        if outputrep.image is None:
            outputrep.image = AImage()
            outputrep.image.save()

        model_image = AImage.objects.create(image=thumb_file)

        outputrep.image.image = thumb_file
        outputrep.image.save()
        outputrep.save()
        print("YES")
    return outputrep

@database_sync_to_async
def get_inputrepresentation_or_error(request: Metamorphing) -> (Representation, np.array):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    inputrep: Representation = request.representation
    if inputrep.nparray is not None:
        array = inputrep.nparray.get_array()
    else:
        #TODO: This should never be called because every representation should have a nparray on creation
        print("ERROR ON INPUTREPRESENTATION")
        array = np.zeros((1024,1024,3))
    if inputrep is None:
        raise ClientError("Inputvid {0} does not exist on Sample {1}".format(str(request.nodeid), request.sample))
    return inputrep, array

@database_sync_to_async
def update_nifti_on_representation(request: Metamorphing, nifti) -> (Representation, str):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    outputrep: Representation = request.representation
    if outputrep is None:
        #TODO make creation of outputvid
        raise ClientError("VID {0} does not exist on Sample {1}".format(str(request.nodeid), request.sample))
    elif outputrep is not None:
        #TODO: update array of output
        niftipath = "representation_nifti/sample_{0}_vid_{1}.nii.gz".format(request.sample_id, request.nodeid)
        niftipath = os.path.join(MEDIA_ROOT, niftipath)
        nib.save(nifti,niftipath)

        nifti = Nifti.objects.create(file=niftipath)
        outputrep.nifti = nifti
        outputrep.nodeid = request.nodeid
        outputrep.save()
        print("YES")
    return outputrep, "update"


@database_sync_to_async
def update_nifti_on_exhibit(request: Metamorphing, nifti) -> (Exhibit, str):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    exhibit: Exhibit = Exhibit.objects.filter(representation=request.representation).filter(nodeid=request.nodeid).first()
    method = "update"
    if exhibit is None:
        #TODO make creation of outputvid
        niftipaths = "sample_{0}_nodeid_{1}.nii.gz".format(request.sample_id, request.nodeid)
        niftipath = os.path.join(NIFTI_ROOT, niftipaths)
        nib.save(nifti, niftipath)
        niftiwebpath = os.path.join(os.path.join(MEDIA_ROOT,"/nifti"),niftipaths)

        exhibit = Exhibit.objects.create(representation=request.representation, creator=request.creator, nodeid=request.nodeid, shape=request.representation.shape,
                                                  sample=request.sample, experiment=request.representation.experiment, niftipath=niftiwebpath)


        print(niftipath)
        exhibit.save()
        method = "create"
    else:
        #TODO: update array of output
        niftipath = "sample_{0}_nodeid_{1}.nii.gz".format(request.sample_id, request.nodeid)
        niftiwebpath = os.path.join(os.path.join(MEDIA_ROOT, "/nifti"), niftipath)
        niftilocalpath = os.path.join(NIFTI_ROOT, niftipath)
        nib.save(nifti, niftilocalpath)
        exhibit.niftipath = niftiwebpath
        exhibit.save()
        print("YES")
    return exhibit, method

@database_sync_to_async
def update_image_on_display(request: Metamorphing, image) -> (Display, str):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    display: Display = Display.objects.filter(representation=request.representation).filter(nodeid=request.nodeid).first()
    method = "update"
    if display is None:
        #TODO make creation of outputvid
        display = Display.objects.create(representation=request.representation, creator=request.creator, nodeid=request.nodeid,
                                                  sample=request.sample, shape=request.representation.shape, experiment=request.representation.experiment)
        method = "create"

    #TODO: update array of output
    path = "sample_{0}_nodeid_{1}".format(str(display.sample.id), str(request.nodeid))
    img_io = io.BytesIO()
    image.save(img_io, format='jpeg', quality=100)
    thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                      img_io.tell, None)

    display.image = thumb_file
    display.save()
    print("YES")
    return display, method

@database_sync_to_async
def update_image_on_representation(request: Metamorphing, convertedfile) -> (Representation, str):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    path = "sample_{0}_vid_{1}".format(str(request.sample.pk), str(request.nodeid))
    outputrep: Representation = request.representation
    if outputrep is None:
        #TODO make creation of outputvid
        raise ClientError("VID {0} does nots exist on Sample {1}".format(str(request.nodeid), request.sample))
    elif outputrep is not None:
        #TODO: update array of output
        img_io = io.BytesIO()
        convertedfile.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)



        model_image = AImage.objects.create(image=thumb_file)
        outputrep.image = model_image
        outputrep.image.save()
        outputrep.nodeid = request.nodeid
        outputrep.save()
        print("YES")
    return outputrep, "update"

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code