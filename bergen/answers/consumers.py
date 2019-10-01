from pandas import DataFrame
from pandas.io.json import json_normalize

from answers.models import Answering, Question
from answers.serializers import AnswerSerializer
from answers.utils import get_answering_or_error, update_answer_or_create
from gql.schema import schema
from transformers.serializers import TransformationSerializer
from trontheim.consumers import OsloJobConsumer


class AnsweringConsumer(OsloJobConsumer):

    async def startparsing(self, data):
        await self.register(data)
        print(data)
        request: Answering = await get_answering_or_error(data["data"])
        settings: dict = await self.getsettings(request.settings, request.oracle.defaultsettings)

        question: Question = request.question
        datapackages = await self.parse(settings,question)

        for datapackage in datapackages:
            key, dataframe = datapackage
            answer, method = await update_answer_or_create(request, settings, key, dataframe)
            await self.modelCreated(answer, AnswerSerializer, method)

    async def parse(self, settings: dict,question: Question) -> DataFrame:
        raise NotImplementedError


    async def getsettings(self, settings: str, defaultsettings: str):
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


class PandaAnswer(AnsweringConsumer):


    async def parse(self, settings: dict, question: Question) -> [DataFrame]:

        query = question.querystring
        print("Executing Schema")
        result = schema.execute(query)

        resultdict = result.to_dict()
        datapackages = []
        data = resultdict["data"]
        for key in data.keys():
            dataframe = json_normalize(data[key])
            datapackages.append((key,dataframe))

        return datapackages

