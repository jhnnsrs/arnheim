import json
import logging

from channels.db import database_sync_to_async

from answers.models import Answering, Answer
from transformers.models import Transforming, Transformation

# Get an instance of a logger
logger = logging.getLogger(__name__)


@database_sync_to_async
def get_answering_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request["id"])
    parsing = Answering.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Answering {0} does not exist".format(str(request["id"])))
    return parsing




@database_sync_to_async
def update_answer_or_create(request: Answering, settings, key, dataframe):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "answer_question-{0}_oracle-{1}_key-{2}_node-{3}".format(str(request.question_id), str(request.oracle_id), str(key),str(request.nodeid))

    answers = Answer.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(answers.count()) if answers.count() else 0)
    vid = vidfirst + vidsub
    answer = answers.last() #TODO: CHeck if that makes sense
    if answer is None or not settings["overwrite"]:
        method = "create"
        logger.info("Creating Pandas with VID: " + vid)
        #TODO make creation of outputvid
        answer = Answer.objects.create(name=request.oracle.name + " of " + request.question.name,
                                       key= key,
                                                       creator=request.creator,
                                                       vid=vid,
                                                       dataframe=dataframe,
                                                       shape=json.dumps(dataframe.shape),
                                                       question=request.question,
                                                       nodeid=request.nodeid)
    elif answer is not None:
        #TODO: update array of output
        method = "update"
        logger.info("Updating Pandas with VID: " + vid)
        #TODO: set name of newly generated and timestamp
        answer.pandas.set_dataframe(dataframe)
        answer.shape = json.dumps(dataframe.shape)
        answer.nodeid = request.nodeid
        answer.save()
    return answer, method



class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code