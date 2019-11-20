import json
from uuid import UUID

from asgiref.sync import async_to_sync
from django.db import models
from channels.layers import get_channel_layer
from rest_framework import viewsets, serializers

channel_layer = get_channel_layer()

# This is necessary so that we serialize the uuid correctly
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class PublishingViewSet(viewsets.ModelViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    publishers = None

    def perform_create(self, serializer):
        super().perform_create(serializer)
        if self.publishers is not None:
            for el in self.publishers:
                try:
                    value = serializer.data[el]
                    path = "{0}_{1}".format(str(el), str(value))
                    print(path)
                    stream = str(serializer.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": "create", "data": serializer.data})
                except KeyError as e:
                    print("Publisher {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))

    def perform_update(self, serializer):
        super().perform_update(serializer)
        if self.publishers is not None:
            for el in self.publishers:
                try:
                    value = serializer.data[el]
                    path = "{0}_{1}".format(str(el), str(value))
                    print(path)
                    stream = str(serializer.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": "update", "data": serializer.data})
                except KeyError as e:
                    print("Publisher {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))

    def perform_destroy(self, instance):
        if self.publishers is not None:
            for el in self.publishers:
                try:
                    serialized = self.serializer_class(instance)
                    value = serialized.data[el]
                    path = "{0}_{1}".format(str(el), str(value))
                    print(path)
                    stream = str(self.serializer_class.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": "delete", "data": serialized.data})
                except KeyError as e:
                    print("Publisher {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))
        super().perform_destroy(instance)


class OsloViewSet(viewsets.ModelViewSet):
    # TODO: The stringpublishing is yet not working

    publishers = None
    viewset_delegates = None
    stringpublish = True

    def publish(self, serializer, method):

        serializedData = serializer.data
        serializedData = json.loads(json.dumps(serializedData, cls=UUIDEncoder)) #Shit workaround to get UUUID to be string

        if self.publishers is not None:
            for el in self.publishers:
                modelfield = "empty"
                try:
                    path = ""
                    for modelfield in el:
                        value = serializedData[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    path = path[:-1]
                    print("Publishing to Models {0}".format(path))
                    stream = str(serializer.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": method, "data": serializedData})
                except KeyError as e:
                    print("Modelfield {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))
                    if self.stringpublish:
                        for modelfield in el:
                            path = modelfield
                            print("Publishing to String {0}".format(path))
                            stream = str(serializer.Meta.model.__name__)
                            async_to_sync(channel_layer.group_send)(path,
                                                                    {"type": "stream", "stream": stream, "room": path,
                                                                     "method": method, "data": serializedData})

    def publishModel(self, model: models.Model, serializerclass: serializers.ModelSerializer.__class__, method: str):
        '''Make sure to call this if you created a new Model on the Database so that the actionpublishers can do their work'''
        serialized = serializerclass(model)
        stream = str(serialized.Meta.model.__name__).lower()
        if stream in self.viewset_delegates.keys():
            print("test")
            self.publishing(serialized, method, self.viewset_delegates[stream], stream)

    def publishing(self, serializer, method, publishers, stream):
        if publishers is not None:
            for el in publishers:
                path = ""
                for modelfield in el:
                    try:
                        value = serializer.data[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    except KeyError as e:
                        print("Modelfield {0} does not exist on {1}".format(str(modelfield), str(stream)))
                        path += "{0}_".format((str(modelfield)))
                path = path[:-1]
                print("Publishing to Channel {0}".format(path))

                async_to_sync(channel_layer.group_send)(
                    path,
                    {
                        "type": "stream",
                        "stream": stream,
                        "room": path,
                        "method": method,
                        "data": serializer.data
                    }
                )

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.publish(serializer, "create")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.publish(serializer, "update")

    def perform_destroy(self, instance):
        serialized = self.serializer_class(instance)
        self.publish(serialized, "delete")
        super().perform_destroy(instance)


class OsloPassThroughViewSet(viewsets.ModelViewSet):
    # TODO: The stringpublishing is yet not working

    publishers = None
    viewset_delegates = None
    stringpublish = True

    def publish(self, serializer, method):
        if self.publishers is not None:
            for el in self.publishers:
                modelfield = "empty"
                try:
                    path = ""
                    for modelfield in el:
                        value = serializer.data[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    path = path[:-1]
                    print("Publishing to Models {0}".format(path))
                    stream = str(serializer.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": method, "data": serializer.data})
                except KeyError as e:
                    print("Modelfield {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))
                    if self.stringpublish:
                        for modelfield in el:
                            path = modelfield
                            print("Publishing to String {0}".format(path))
                            stream = str(serializer.Meta.model.__name__)
                            async_to_sync(channel_layer.group_send)(path,
                                                                    {"type": "stream", "stream": stream, "room": path,
                                                                     "method": method, "data": serializer.data})

    def publishModel(self, model: models.Model, serializerclass: serializers.ModelSerializer.__class__, method: str):
        '''Make sure to call this if you created a new Model on the Database so that the actionpublishers can do their work'''
        serialized = serializerclass(model)
        stream = str(serialized.Meta.model.__name__).lower()
        if stream in self.viewset_delegates.keys():
            print("test")
            self.publishing(serialized, method, self.viewset_delegates[stream], stream)

    def publishing(self, serializer, method, publishers, stream):
        if publishers is not None:
            for el in publishers:
                path = ""
                for modelfield in el:
                    try:
                        value = serializer.data[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    except KeyError as e:
                        print("Modelfield {0} does not exist on {1}".format(str(modelfield), str(stream)))
                        path += "{0}_".format((str(modelfield)))
                path = path[:-1]
                print("Publishing to Channel {0}".format(path))

                async_to_sync(channel_layer.group_send)(
                    path,
                    {
                        "type": "stream",
                        "stream": stream,
                        "room": path,
                        "method": method,
                        "data": serializer.data
                    }
                )

    def perform_create(self, serializer):
        self.publish(serializer, "create")

    def perform_update(self, serializer):
        self.publish(serializer, "update")

    def perform_destroy(self, instance):
        serialized = self.serializer_class(instance)
        self.publish(serialized, "delete")


class OsloJob(object):

    def __init__(self, data=None, actiontype=None, actionpublishers=None, job=None, channel=None):
        self.actiontype = actiontype
        self.data = data
        self.job = job if job else data
        self.actionpublishers = actionpublishers
        self.channel = channel


class OsloActionViewSet(OsloViewSet):
    actionpublishers = None  # this publishers will be send to the Action Handles and then they can send to the according
    channel = None
    actiontype = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def preprocess_jobs(self, serializer):
        """ If you need to alter any data like creating an Model on the fly
         or create various jobs from one request, here is the place
         should return Array of Jobs that need executing"""
        return [self.create_job(serializer.data)]

    def create_job(self, data, actiontype=None, actionpublishers=None, job=None, channel=None) -> OsloJob:
        actiontype = actiontype if actiontype else self.actiontype
        actionpublishers = actionpublishers if actionpublishers else self.actionpublishers
        job = job if job else data
        channel = channel if channel else self.channel
        return OsloJob(data, actiontype, actionpublishers, job, channel)

    def perform_create(self, serializer):
        """ Right now only the creation of a new Job is possible, no way of stopping a job on its way"""
        serializer.save()
        jobs = self.preprocess_jobs(serializer)
        self.publish_jobs(jobs)
        self.publish(serializer, "create")

    def publish_jobs(self, jobs: [OsloJob]):
        for nana in jobs:
            async_to_sync(channel_layer.send)(nana.channel, {"type": nana.actiontype, "data": nana.data,
                                                             "publishers": nana.actionpublishers, "job": nana.job})
