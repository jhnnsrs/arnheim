from typing import Callable, Awaitable, Any, Dict

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.db import models
from rest_framework import serializers

from larvik.logging import get_module_logger


class LarvikError(Exception):

    def __init__(self, message):
        self.message = message



class StatusCode(object):
    STARTED = 2000
    DONE = 1000
    PROGRESS = 3000
    ERROR = 4000


class Messages(object):
    STARTED = "Starting"
    ERROR = "Error"
    PROGRESS = "Progress"
    DONE = "Done"

    @staticmethod
    def error(message) -> str:
        return Messages.ERROR + " - " + str(message)

    @staticmethod
    def progress(percent) -> str:
        return Messages.PROGRESS + " - " + str(percent)

class LarvikStatus(object):

    def __init__(self,code: int, message: str = None):
        self.statuscode = code
        self.message = message if message is not None else ""

def larvikError(message = None):
    return LarvikStatus(StatusCode.ERROR,message)

def larvikProgress(message = None):
    return LarvikStatus(StatusCode.PROGRESS,message)

def larvikDone(message = None):
    return LarvikStatus(StatusCode.DONE,message)

@database_sync_to_async
def update_status_on_larvikjob(parsing, status: LarvikStatus):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    parsing.statuscode = status.statuscode
    parsing.statusmessage = status.message
    parsing.save()
    return parsing

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

                await self.channel_layer.group_send(
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
        self.request = await self.updateRequestFunction()(self.request,larvikProgress(progressMessage))
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
        await self.updateRequest(LarvikStatus(StatusCode.STARTED,"Started"))

        # TODO: Impelement with a request Parentclass
        self.settings: dict = self.getsettings(self.request.settings, self.getDefaultSettings(self.request))


        try:
            returndict = await self.parse(self.request, self.settings)


            for modelname, modelparams in returndict.items():
                models = await self.getModelFuncDict()[modelname](modelparams,self.request,self.settings)
                for (model, method ) in models:
                    await self.modelCreated(model, self.getSerializerDict()[type(model).__name__], method)
                    self.logger.info(method + " Model " + modelname)

            await self.updateRequest(LarvikStatus(StatusCode.DONE,"Done"))

        except LarvikError as e:
            self.logger.error(e)
            await self.updateRequest(LarvikStatus(StatusCode.ERROR,e.message))
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

