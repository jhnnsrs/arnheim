from typing import Callable, Awaitable, Any, Dict, List, Tuple

from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.layers import get_channel_layer
from dask.distributed import Client
from django.db import models
from django.db.models import Model
from rest_framework import serializers

from larvik.logging import get_module_logger
from larvik.models import LarvikJob
from larvik.structures import StatusCode, LarvikStatus, larvikError, larvikProgress

channel_layer = get_channel_layer()

class LarvikError(Exception):

    def __init__(self, message):
        self.message = message


class LarvikConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.publishers = None
        self.job = None
        self.data = None
        self.request = None
        self.requestSerializer = None
        self.logger = get_module_logger(type(self).__name__)


    def register(self,data):
        self.publishers = dict(data["publishers"])
        self.job = data["job"]
        self.data = data

    async def modelCreated(self, model: models.Model, serializerclass: serializers.ModelSerializer.__class__, method: str):
        '''Make sure to call this if you created a new Model on the Database so that the actionpublishers can do their work'''
        serialized = serializerclass(model)
        stream = str(type(model).__name__).lower()
        if stream in self.publishers.keys():
            self.logger.info("Found stream {0} in Publishers. Tyring to publish".format(str(stream)))
            await self.publish(serialized, method,self.publishers[stream],stream)

    async def publish(self,serializer, method, publishers,stream):
        if publishers is not None:
            for el in publishers:
                path = ""
                for modelfield in el:
                    try:
                        value = serializer.data[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    except:
                        self.logger.info("Modelfield {0} does not exist on {1}".format(str(modelfield), str(stream)))
                        path += "{0}_".format((str(modelfield)))
                path = path[:-1] # Trim the last underscore

                self.logger.info("Publishing to Channel {0}".format(path))

                await channel_layer.group_send(
                    path,
                    {
                        "type": "stream",
                        "stream": stream,
                        "room": path,
                        "method": method,
                        "data": serializer.data
                    }
                )


    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        '''Should return a Function that returns the Model and not the Serialized instance'''
        raise NotImplementedError

    def updateRequestFunction(self) -> Callable[[models.Model,str], Awaitable[models.Model]]:
        '''Should update the Status (provided as string) on the Model and return the Model'''
        raise NotImplementedError

    def getModelFuncDict(self) -> Dict[str,Callable[[Any,models.Model,dict], Awaitable[Any]]]:
        ''' Should return a dict with key: modelname, value: awaitable Model Updater that returns a Modelinstance and the method of database propagation'''
        raise NotImplementedError

    def getSerializerDict(self) -> Dict[str,type(serializers.Serializer)]:
        ''' Should return a dict with key: modelname, value: serializerClass (no instance)'''
        raise NotImplementedError

    def getDefaultSettings(self, request: models.Model) -> str:
        ''' Should return the Defaultsettings as a JSON parsable String'''


    async def progress(self,value, message=None):
        if self.requestSerializer is None: self.requestSerializer = self.getSerializerDict()[type(self.request).__name__]
        progressMessage = value if message is None else "{0} % - {1}".format(value, message)
        self.request = await self.updateRequestFunction()(self.request, larvikProgress(progressMessage))
        self.logger.info("Updating Progress to {0} with message {1}".format(str(value),str(message)))
        await self.modelCreated(self.request, self.requestSerializer, "update")

    async def updateRequest(self, status: LarvikStatus):
        # Classic Update Circle
        if self.requestSerializer is None: self.requestSerializer = self.getSerializerDict()[type(self.request).__name__]
        self.request = await self.updateRequestFunction()(self.request, status)
        await self.modelCreated(self.request, self.requestSerializer, "update")

    async def startJob(self, data):

        self.register(data)
        self.logger.info("Received Data")

        # Working on models is easier, so the cost of a database call is bearable
        self.request: models.Model = await self.getRequestFunction()(data["data"])
        await self.updateRequest(LarvikStatus(StatusCode.STARTED, "Started"))

        # TODO: Impelement with a request Parentclass
        self.settings: dict = self.getsettings(self.request.settings, self.getDefaultSettings(self.request))


        try:
            returndict = await self.parse(self.request, self.settings)


            for modelname, modelparams in returndict.items():
                models = await self.getModelFuncDict()[modelname](modelparams,self.request,self.settings)
                for (model, method ) in models:
                    await self.modelCreated(model, self.getSerializerDict()[type(model).__name__], method)
                    self.logger.info(str(method).capitalize() + " Model " + type(model).__name__)

            await self.updateRequest(LarvikStatus(StatusCode.DONE, "Done"))

        except LarvikError as e:
            self.logger.error(e)
            await self.updateRequest(LarvikStatus(StatusCode.ERROR, e.message))
        except Exception as e:
            self.logger.error(e)
            await self.updateRequest(LarvikStatus(StatusCode.ERROR, "Uncaught Error on Server, check log there"))

    async def parse(self, request: models.Model, settings: dict) -> Dict[str, Any]:
        """ If you create objects make sure you are handling them in here
        and publish if necessary with its serializer """
        raise NotImplementedError

    def getsettings(self, settings: str, defaultsettings: str):
        """Updateds the Settings with the Defaultsettings"""
        import json
        try:
            settings = json.loads(settings)
            try:
                defaultsettings = json.loads(defaultsettings)
            except:
                defaultsettings = {}

        except:
            defaultsettings = {}
            settings = {}

        defaultsettings.update(settings)
        return defaultsettings


class AsyncLarvikConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.publishers = None
        self.job = None
        self.data = None
        self.request = None
        self.requestSerializer = None
        self.logger = get_module_logger(type(self).__name__)


    def register(self,data):
        self.publishers = dict(data["publishers"])
        self.job = data["job"]
        self.data = data

    async def updateModel(self,model: models.Model, method: str):
        await self.modelCreated(model, self.getSerializers()[type(model).__name__], method)


    async def modelCreated(self, model: models.Model, serializerclass: serializers.ModelSerializer.__class__, method: str):
        '''Make sure to call this if you created a new Model on the Database so that the actionpublishers can do their work'''
        serialized = serializerclass(model)
        stream = str(type(model).__name__).lower()
        if stream in self.publishers.keys():
            self.logger.info("Found stream {0} in Publishers. Tyring to publish".format(str(stream)))
            await self.publish(serialized, method,self.publishers[stream],stream)

    async def publish(self,serializer, method, publishers,stream):
        if publishers is not None:
            for el in publishers:
                path = ""
                for modelfield in el:
                    try:
                        value = serializer.data[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    except:
                        self.logger.info("Modelfield {0} does not exist on {1}".format(str(modelfield), str(stream)))
                        path += "{0}_".format((str(modelfield)))
                path = path[:-1] # Trim the last underscore

                self.logger.info("Publishing to Channel {0}".format(path))

                await channel_layer.group_send(
                    path,
                    {
                        "type": "stream",
                        "stream": stream,
                        "room": path,
                        "method": method,
                        "data": serializer.data
                    }
                )


    def getRequestFunction(self) -> Callable[[Dict], Awaitable[LarvikJob]]:
        '''Should return a Function that returns the Model and not the Serialized instance'''
        raise NotImplementedError

    def updateRequestFunction(self) -> Callable[[models.Model,str], Awaitable[models.Model]]:
        '''Should update the Status (provided as string) on the Model and return the Model'''
        raise NotImplementedError

    def getSerializers(self) -> Dict[str,type(serializers.Serializer)]:
        ''' Should return a dict with key: modelname, value: serializerClass (no instance)'''
        raise NotImplementedError

    def getDefaultSettings(self, request: models.Model) -> Dict:
        ''' Should return the Defaultsettings as a JSON parsable String'''
        raise NotImplementedError


    async def progress(self,message=None):
        self.logger.info(f"Progress {message}")
        await self.updateRequest(larvikProgress(message))

    async def updateRequest(self, status: LarvikStatus):
        # Classic Update Circle
        if self.requestSerializer is None: self.requestSerializer = self.getSerializers()[type(self.request).__name__]
        self.request = await self.updateRequestFunction()(self.request, status)
        await self.modelCreated(self.request, self.requestSerializer, "update")


    async def start(self,request: LarvikJob, settings: Dict):
        raise NotImplementedError

    async def startJob(self, data):

        self.register(data)
        self.logger.info("Received Data")
        # Working on models is easier, so the cost of a database call is bearable
        self.request: LarvikJob = await self.getRequestFunction()(data["data"])
        await self.updateRequest(LarvikStatus(StatusCode.STARTED, "Started"))


        # TODO: Impelement with a request Parentclass
        self.settings: dict = self._getsettings(self.request.settings, self.getDefaultSettings(self.request))

        try:
            await self.start(self.request, self.settings)
            await self.updateRequest(LarvikStatus(StatusCode.DONE, "Done"))
        except LarvikError as e:
            self.logger.error(e)
            await self.updateRequest(LarvikStatus(StatusCode.ERROR, e.message))
        except Exception as e:
            self.logger.error(e)
            await self.updateRequest(LarvikStatus(StatusCode.ERROR, "Uncaught Error on Server, check log there"))


    def _getsettings(self, settings: str, defaultsettings: Dict):
        """Updateds the Settings with the Defaultsettings"""
        import json
        try:
            settings = json.loads(settings)
            try:
                defaultsettings = defaultsettings
            except:
                defaultsettings = {}

        except:
            defaultsettings = {}
            settings = {}

        defaultsettings.update(settings)
        return defaultsettings


class ModelFuncAsyncLarvikConsumer(AsyncLarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[LarvikJob]]:
        raise NotImplementedError

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        raise NotImplementedError

    def getSerializers(self) -> Dict[str, type(serializers.Serializer)]:
        raise NotImplementedError

    def getDefaultSettings(self, request: models.Model) -> Dict:
        raise NotImplementedError

    def getModelFuncDict(self):
        raise NotImplementedError

    async def parse(self, request: LarvikJob, settings: dict) -> Dict[str, Any]:
        raise NotImplementedError

    async def start(self, request: LarvikJob, settings: Dict):
        try:
            returndict = await self.parse(self.request, self.settings)

            for modelname, modelparams in returndict.items():
                models = await self.getModelFuncDict()[modelname](modelparams, self.request, self.settings)
                for (model, method) in models:
                    await self.updateModel(model, method)

            await self.updateRequest(LarvikStatus(StatusCode.DONE, "Done"))

        except LarvikError as e:
            self.logger.error(e)
            await self.updateRequest(LarvikStatus(StatusCode.ERROR, e.message))
        except Exception as e:
            self.logger.error(e)
            await self.updateRequest(LarvikStatus(StatusCode.ERROR, "Uncaught Error on Server, check log there"))


class SyncLarvikConsumer(SyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.publishers = None
        self.job = None
        self.data = None
        self.request = None
        self.requestSerializer = None
        self.logger = get_module_logger(type(self).__name__)


    def register(self,data):
        self.publishers = dict(data["publishers"])
        self.job = data["job"]
        self.data = data

    def updateModel(self,model: models.Model, method: str):
        return self.modelCreated(model, self.getSerializers()[type(model).__name__], method)

    def modelCreated(self, model: models.Model, serializerclass: serializers.ModelSerializer.__class__, method: str):
        '''Make sure to call this if you created a new Model on the Database so that the actionpublishers can do their work'''
        serialized = serializerclass(model)
        stream = str(type(model).__name__).lower()
        if stream in self.publishers.keys():
            self.logger.info("Found stream {0} in Publishers. Tyring to publish".format(str(stream)))
            self.publish(serialized, method,self.publishers[stream],stream)

    def progress(self,message=None):
        self.logger.info(f"Progress {message}")
        self.updateStatus(larvikProgress(message=message))

    def publish(self,serializer, method, publishers,stream):
        if publishers is not None:
            for el in publishers:
                path = ""
                for modelfield in el:
                    try:
                        value = serializer.data[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    except:
                        self.logger.info("Modelfield {0} does not exist on {1}".format(str(modelfield), str(stream)))
                        path += "{0}_".format((str(modelfield)))
                path = path[:-1] # Trim the last underscore

                self.logger.info("Publishing to Channel {0}".format(path))

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


    def getRequest(self,data) -> LarvikJob:
        '''Should return a Function that returns the Model and not the Serialized instance'''
        raise NotImplementedError

    def getSerializers(self):
        '''Should return a Function that returns the Model and not the Serialized instance'''
        raise NotImplementedError

    def updateStatus(self, status: LarvikStatus):
        # Classic Update Circle
        if self.requestSerializer is None: self.requestSerializer = self.getSerializers()[type(self.request).__name__]
        self.request.statuscode = status.statuscode
        self.request.statusmessage = status.message
        self.request.save()
        self.modelCreated(self.request, self.requestSerializer, "update")


    def getDefaultSettings(self, request: models.Model) -> Dict:
        ''' Should return the Defaultsettings as a JSON parsable String'''
        raise NotImplementedError

    def start(self,request: LarvikJob, settings: dict):
        raise NotImplementedError


    def startJob(self, data):

        self.register(data)
        self.logger.info("Received Data")

        # Working on models is easier, so the cost of a database call is bearable
        self.request: LarvikJob = self.getRequest(data["data"])

        # TODO: Impelement with a request Parentclass
        self.settings: dict = self._getsettings(self.request.settings, self.getDefaultSettings(self.request))
        self.progress("Settings Loaded")

        try:
            self.start(self.request,self.settings)
            self.updateStatus(LarvikStatus(StatusCode.DONE, "Done"))
        except LarvikError as e:
            self.logger.error(e)
            self.updateStatus(larvikError(repr(e)))
        except Exception as e:
            self.logger.error(e)
            self.updateStatus(larvikError(repr(e)))


    def _getsettings(self, settings: str, defaultsettings: Dict):
        """Updateds the Settings with the Defaultsettings"""
        import json
        try:
            settings = json.loads(settings)
            try:
                defaultsettings = defaultsettings
            except:
                defaultsettings = {}

        except:
            defaultsettings = {}
            settings = {}

        defaultsettings.update(settings)
        return defaultsettings


class DaskSyncLarvikConsumer(SyncLarvikConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.c = Client()

    def getRequest(self, data) -> LarvikJob:
        raise NotImplementedError

    def getSerializers(self):
        raise NotImplementedError

    def getDefaultSettings(self, request: models.Model) -> Dict:
        raise NotImplementedError

    def parse(self, request: LarvikJob, settings: dict) -> List[Tuple[models.Model,str]]:
        raise NotImplementedError

    def start(self, request: LarvikJob, settings: dict):
        try:
            returndict = self.parse(self.request, self.settings)

            for item in returndict:
                model, method = item
                self.modelCreated(model, self.getSerializers()[type(model).__name__], method)
                self.logger.info(str(method).capitalize() + " Model " + type(model).__name__)


        except FileNotFoundError as e:
            self.logger.info("RETRYING")
            self.start(request,settings)  # recuversive


class DaskLarvikConsumer(SyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.publishers = None
        self.job = None
        self.data = None
        self.request = None
        self.requestSerializer = None
        self.logger = get_module_logger(type(self).__name__)
        self.c = Client()


    def register(self,data):
        self.publishers = dict(data["publishers"])
        self.job = data["job"]
        self.data = data

    def modelCreated(self, model: models.Model, serializerclass: serializers.ModelSerializer.__class__, method: str):
        '''Make sure to call this if you created a new Model on the Database so that the actionpublishers can do their work'''
        serialized = serializerclass(model)
        stream = str(type(model).__name__).lower()
        if stream in self.publishers.keys():
            self.logger.info("Found stream {0} in Publishers. Tyring to publish".format(str(stream)))
            self.publish(serialized, method,self.publishers[stream],stream)

    def progress(self,message=None):
        self.logger.info(f"Progress {message}")
        self.updateStatus(larvikProgress(message=message))

    def publish(self,serializer, method, publishers,stream):
        if publishers is not None:
            for el in publishers:
                path = ""
                for modelfield in el:
                    try:
                        value = serializer.data[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    except:
                        self.logger.info("Modelfield {0} does not exist on {1}".format(str(modelfield), str(stream)))
                        path += "{0}_".format((str(modelfield)))
                path = path[:-1] # Trim the last underscore

                self.logger.info("Publishing to Channel {0}".format(path))

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


    def getRequest(self,data) -> LarvikJob:
        '''Should return a Function that returns the Model and not the Serialized instance'''
        raise NotImplementedError

    def getSerializers(self):
        '''Should return a Function that returns the Model and not the Serialized instance'''
        raise NotImplementedError

    def updateStatus(self, status: LarvikStatus):
        # Classic Update Circle
        if self.requestSerializer is None: self.requestSerializer = self.getSerializers()[type(self.request).__name__]
        self.request.statuscode = status.statuscode
        self.request.statusmessage = status.message
        self.request.save()
        self.modelCreated(self.request, self.requestSerializer, "update")


    def getDefaultSettings(self, request: models.Model) -> Dict:
        ''' Should return the Defaultsettings as a JSON parsable String'''
        raise NotImplementedError


    def startJob(self, data):

        self.register(data)
        self.logger.info("Received Data")

        # Working on models is easier, so the cost of a database call is bearable
        self.request: LarvikJob = self.getRequest(data["data"])

        # TODO: Impelement with a request Parentclass
        self.settings: dict = self.getsettings(self.request.settings, self.getDefaultSettings(self.request))
        self.progress("Settings Loaded")

        try:
            returndict = self.parse(self.request, self.settings)

            for item in returndict:
                model, method = item
                self.modelCreated(model, self.getSerializers()[type(model).__name__], method)
                self.logger.info(str(method).capitalize() + " Model " + type(model).__name__)


        except FileNotFoundError as e:
            self.logger.info("RETRYING")
            self.startJob(data) #recuversive
        except LarvikError as e:
            self.logger.error(e)
            self.updateStatus(larvikError(repr(e)))
        except Exception as e:
            self.logger.error(e)
            self.updateStatus(larvikError(repr(e)))
            raise e

    def parse(self, request: LarvikJob, settings: dict) -> List[Tuple[str, Any]]:
        """ If you create objects make sure you are handling them in here
        and publish if necessary with its serializer """
        raise NotImplementedError

    def getsettings(self, settings: str, defaultsettings: Dict):
        """Updateds the Settings with the Defaultsettings"""
        import json
        try:
            settings = json.loads(settings)
            try:
                defaultsettings = defaultsettings
            except:
                defaultsettings = {}

        except:
            defaultsettings = {}
            settings = {}

        defaultsettings.update(settings)
        return defaultsettings

