from typing import Dict, Any, Callable, Awaitable

from django.db import models
from pandas.io.json import json_normalize
from rest_framework import serializers

from answers.models import Answering
from answers.serializers import AnswerSerializer, AnsweringSerializer
from answers.utils import get_answering_or_error, answer_update_or_create
from gql.schema import schema
from larvik.consumers import LarvikConsumer, update_status_on_larvikjob

class PandaAnswer(LarvikConsumer):

    def getRequestFunction(self) -> Callable[[Dict], Awaitable[models.Model]]:
        return get_answering_or_error

    def updateRequestFunction(self) -> Callable[[models.Model, str], Awaitable[models.Model]]:
        return update_status_on_larvikjob

    def getModelFuncDict(self) -> Dict[str, Callable[[Any, models.Model, dict], Awaitable[Any]]]:
        return {
            "datapackage": answer_update_or_create
        }

    def getSerializerDict(self) -> Dict[str, type(serializers.Serializer)]:
        return {
            "Answer": AnswerSerializer,
            "Answering": AnsweringSerializer
        }

    async def parse(self, request: Answering, settings: dict) -> Dict[str, Any]:
        query = request.question.querystring
        self.logger.info("Executing Schema")
        await self.progress(20, "Querying Schema")
        result = schema.execute(query)

        resultdict = result.to_dict()
        datapackages = []
        data = resultdict["data"]
        await self.progress(80, "Creating Answers")
        for key in data.keys():
            dataframe = json_normalize(data[key])
            datapackages.append((key, dataframe))

        return {"datapackage": datapackages}




