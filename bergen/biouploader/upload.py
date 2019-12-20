import os
import shutil

from biouploader.models import BioImage
from mandal.settings import BIOIMAGE_ROOT

logger = get_module_logger(__name__)
def move_upload_to_storage(source, name, creatorid, lockerid):
    '''moving an uploaded file (from nginx module) to storage means.
         1. create a folder for the collection, if doesn't exist
         2. an image in storage pointing to the moved file
         Parameters
         ==========
         collection: the collection the image will belong to
         source: the source file (under /var/www/images/_upload/{0-9}
         dest: the destination filename
         :param creatorid:
    '''
    directory = "{0}/{1}/".format(creatorid, lockerid)
    directory = os.path.join(BIOIMAGE_ROOT, directory)

    if not os.path.exists(directory):
        os.makedirs(directory)

    new_path = os.path.join(directory, os.path.basename(name))
    shutil.move(source, new_path)
    return new_path


def moveFileToLocker(path, creator, locker, name=None):
    '''Attention this can only be called by the notebook instance
       Attention this can only be called by the notebook instance
       Parameters
       ==========
       path: the path to the file uploaded
       name: the requested name for the container
       version: the md5 sum of the file
       size: the file size. if not provided, is calculated
    '''

    # Media Path of Nginx is solely MEDIA, this one here is /code/media

    if os.path.exists(path):
        print("Moved file from " + path)
        new_path = move_upload_to_storage(path, name, creator, locker)
        print("To New Path of " + new_path)
        name = name if name else os.path.basename(path)
        image = BioImage.objects.create(file=new_path,
                                        creator_id=creator,
                                        locker_id=locker,
                                        name=os.path.basename(name))

        image.save()
        return image




