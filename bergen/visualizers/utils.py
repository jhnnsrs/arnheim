import logging
import os

from channels.db import database_sync_to_async
from pandas import DataFrame

from mandal.settings import PROFILES_ROOT, EXCELS_ROOT
# Get an instance of a logger
from visualizers.managers import toFileName, toExcelFileName
from visualizers.models import Visualizing, Profile, ExcelExport

logger = logging.getLogger(__name__)


@database_sync_to_async
def get_visualizing_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    print(request["id"])
    parsing = Visualizing.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("Visualizing {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def update_status_on_visualizing(parsing, status):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing.status = status
    parsing.save()
    return parsing




@database_sync_to_async
def update_profile_or_create(request: Visualizing, settings, report):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "profile_answer-{0}_node-{1}".format(str(request.answer_id),str(request.nodeid))
    profiles = Profile.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(profiles.count()) if profiles.count() else 0)
    vid = vidfirst + vidsub
    profile = profiles.last() #TODO: CHeck if that makes sense
    if profile is None or not settings["overwrite"]:
        method = "create"
        logger.info("Creating Report with VID: " + vid)
        #TODO make creation of outputvid
        profile = Profile.objects.create(name=request.visualizer.name + " of " + request.answer.name,
                                         creator=request.creator,
                                         vid=vid,
                                         report=report,
                                         answer=request.answer,
                                         nodeid=request.nodeid)
    elif profile is not None:
        #TODO: update array of output
        method = "update"
        logger.info("Updating Report with VID: " + vid)
        #TODO: set name of newly generated and timestamp
        joinedpath = os.path.join(PROFILES_ROOT, toFileName(vid))
        report.to_file(joinedpath)
        profile.nodeid = request.nodeid
        profile.save()
    return profile, method

@database_sync_to_async
def update_excelexport_or_create(request: Visualizing, settings, report: DataFrame):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    method = "error"
    vidfirst = "excel_answer-{0}_node-{1}".format(str(request.answer_id),str(request.nodeid))
    excels = ExcelExport.objects.filter(vid__startswith=vidfirst)
    vidsub = "_{0}".format(str(excels.count()) if excels.count() else 0)
    vid = vidfirst + vidsub
    excel = excels.last() #TODO: CHeck if that makes sense
    if excel is None or not settings["overwrite"]:
        method = "create"
        logger.info("Creating Excel with VID: " + vid)
        #TODO make creation of outputvid
        excel = ExcelExport.objects.create(name=request.visualizer.name + " of " + request.answer.name,
                                         creator=request.creator,
                                         vid=vid,
                                         report=report,
                                         answer=request.answer,
                                         nodeid=request.nodeid)
    elif excel is not None:
        #TODO: update array of output
        method = "update"
        logger.info("Updating Excel with VID: " + vid)
        #TODO: set name of newly generated and timestamp
        joinedpath = os.path.join(EXCELS_ROOT, toExcelFileName(vid))
        report.to_excel(joinedpath)
        excel.nodeid = request.nodeid
        excel.save()
    return excel, method



class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code