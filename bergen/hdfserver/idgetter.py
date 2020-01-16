"""
Helper function - get uuid for a given path
"""
from rest_framework.exceptions import APIException

from elements.models import Numpy

"""
    Helper function - get endpoint we'll send http requests to 
"""
##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of H5Serv (HDF5 REST Server) Service, Libraries and      #
# Utilities.  The full HDF5 REST Server copyright notice, including          #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################
import six

if six.PY3:
    unicode = str

import json
import base64
from mandal import settings
import requests
# import the logging library
import logging
import os


logger = logging.getLogger(__name__)
host = settings.HDFSERVER["host"]
port = settings.HDFSERVER["port"]



def getEndpoint():
    endpoint = 'http://' + host + ':' + str(port)
    return endpoint


"""
Helper function - return true if the parameter looks like a UUID
"""


def validateId(id):
    if type(id) != str and type(id) != unicode:
        # should be a string
        return False
    if len(id) != 36:
        # id's returned by uuid.uuid1() are always 36 chars long
        return False
    return True


"""
Helper function - get auth string
"""


def getAuthString(user, password):
    auth_string = user + ':' + password
    auth_string = auth_string.encode('utf-8')
    auth_string = base64.b64encode(auth_string)
    auth_string = b"Basic " + auth_string
    return auth_string


"""
Helper function - get root uuid  
"""


def getRootUUID(domain, user=None, password=None):
    req = getEndpoint() + "/"
    headers = {'host': domain}
    if user is not None:
        # if user is supplied, add the auth header
        headers['Authorization'] = getAuthString(user, password)
    rsp = requests.get(req, headers=headers)
    rootUUID = None
    if rsp.status_code == 200:
        rspJson = json.loads(rsp.text)
        rootUUID = rspJson["root"]
    print(rsp.status_code)
    return rootUUID


def getUUIDByPath(domain, path, user=None, password=None):
    if path[0] != '/':
        raise KeyError("only abs paths")  # only abs paths

    parent_uuid = getRootUUID(domain, user=user, password=password)

    if path == '/':
        return parent_uuid

    headers = {'host': domain}
    if user is not None:
        # if user is supplied, add the auth header
        headers['Authorization'] = getAuthString(user, password)

    # make a fake tgt_json to represent 'link' to root group
    tgt_json = {'collection': "groups", 'class': "H5L_TYPE_HARD", 'id': parent_uuid}
    tgt_uuid = None

    names = path.split('/')

    for name in names:
        if not name:
            continue
        if parent_uuid is None:
            raise KeyError("not found")

        req = getEndpoint() + "/groups/" + parent_uuid + "/links/" + name
        rsp = requests.get(req, headers=headers)
        if rsp.status_code != 200:
            raise KeyError("not found")
        rsp_json = json.loads(rsp.text)
        tgt_json = rsp_json['link']

        if tgt_json['class'] == 'H5L_TYPE_HARD':
            # print "hard link, collection:", link_json['collection']
            if tgt_json['collection'] == 'groups':
                parent_uuid = tgt_json['id']
            else:
                parent_uuid = None
            tgt_uuid = tgt_json['id']
        else:
            raise KeyError("non-hard link")
    return tgt_uuid

class HDFException(APIException):
    status_code = 503
    default_detail = 'HDF Service malfunctioning temporarily, try again later.'
    default_code = 'service_unavailable'



def getDataSetUUIDforNumpy(numpy: Numpy):

    ## This is a dirty hack to get the correct filepath for the old samplefiles
    ## New Ones should be safed as sample-{id} and not face weird number errors
    filename = os.path.basename(numpy.filepath)
    fnwithoutextenstion = os.path.splitext(filename)[0].replace(".", "%2E")

    domain = "{0}.h5files.{1}".format(fnwithoutextenstion, host)
    headers = {"host": domain}
    type = numpy.type
    vid = numpy.vid
    logger.info("Trying to get Dataset {0} of Type {1} from Domain: {2}".format(vid,type,domain))
    try:
        datasetid = getUUIDByPath(domain, "/{0}/{1}".format(type, vid))
    except KeyError as e:
        logger.error("The File seems not to be updated Try updating")
        reg = 'http://' + host + ':' + str(port) + "/update"
        updated = requests.get(reg, headers=headers)
        if updated.status_code == 200:
            datasetid = getUUIDByPath(domain, "/{0}/{1}".format(type, vid))
        else:
            logger.error("Something is wrong, we are not able to get the dataset")
            raise HDFException()

    return (domain, datasetid)


def queryDataSetUUID(domain, datasetid, query):
    reg = 'http://' + host + ':' + str(port) + "/datasets/" + datasetid + "/"+ query
    headers = {"host": domain}
    answer = requests.get(reg, headers=headers)
    return answer