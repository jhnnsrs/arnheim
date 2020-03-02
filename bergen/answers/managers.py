from django.db import models

from elements.models import Pandas
from larvik.logging import get_module_logger
from django.conf import settings

logger = get_module_logger(__name__)

class AnswerManager(models.Manager):
    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        if "dataframe" in obj_data:
            logger.info("Creating Pandas with help of HDFStore")
            vid = str(obj_data["vid"])

            # TODO: if sample is not provided this should raise an exception
            panda = Pandas.objects.create(vid=vid, dataframe=obj_data["dataframe"], type="transformations", compression=obj_data.get("compression",settings.PANDAS_COMPRESSION), answer=obj_data["name"])

            obj_data["pandas"] = panda
            del obj_data["dataframe"]

        # Now call the super method which does the actual creation
        return super().create(**obj_data)  # Python 3 syntax!!