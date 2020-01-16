import logging
import os

from django.db import models

from mandal import settings
# Get an instance of a logger
from mandal.settings import MEDIA_URL

logger = logging.getLogger(__name__)


def toFileName(vid):
    return vid + ".html"

def toExcelFileName(vid):
    return vid + ".xlsx"

class ProfileManager(models.Manager):
    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        if "report" in obj_data:
            print("Saving Report with help of")
            vid = str(obj_data["vid"])

            joinedpath = os.path.join(settings.PROFILES_ROOT, toFileName(vid))
            if not os.path.exists(settings.PROFILES_ROOT):
                logger.warning("Creating Directory for Profiles" + str(settings.PROFILES_ROOT))
                os.makedirs(settings.PROFILES_ROOT)

            report = obj_data["report"]
            report.to_file(output_file=joinedpath)
            # TODO: if sample is not provided this should raise an exception


            obj_data["htmlfile"] = os.path.join(os.path.join(MEDIA_URL,"/profiles"),toFileName(vid))
            del obj_data["report"]

        # Now call the super method which does the actual creation
        return super().create(**obj_data)  # Python 3 syntax!!


class ExcelExportManager(models.Manager):
    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        if "report" in obj_data:
            print("Saving Report with help of")
            vid = str(obj_data["vid"])

            joinedpath = os.path.join(settings.EXCELS_ROOT, toExcelFileName(vid))
            if not os.path.exists(settings.EXCELS_ROOT):
                logger.warning("Creating Directory for Excels" + str(settings.EXCELS_ROOT))
                os.makedirs(settings.EXCELS_ROOT)

            report = obj_data["report"]
            report.to_excel(joinedpath)
            # TODO: if sample is not provided this should raise an exception


            obj_data["excelfile"] = os.path.join(os.path.join(MEDIA_URL,"/excels"),toExcelFileName(vid))
            del obj_data["report"]

        # Now call the super method which does the actual creation
        return super().create(**obj_data)  # Python 3 syntax!!