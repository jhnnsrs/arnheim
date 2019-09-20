import os
import shutil

from biouploader.models import BioImage
from multichat.settings import MEDIA_ROOT


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
    directory = "bioimages/{0}/{1}/".format(creatorid, lockerid)
    directory = os.path.join(MEDIA_ROOT,directory)

    if not os.path.exists(directory):
        os.makedirs(directory)

    new_path = os.path.join(directory, os.path.basename(name))
    shutil.move(source, new_path)
    return new_path


def upload_file(name, version, path, size, experiment, creator, locker):
    '''save an uploaded container, usually coming from an ImageUpload
       Parameters
       ==========
       path: the path to the file uploaded
       name: the requested name for the container
       version: the md5 sum of the file
       size: the file size. if not provided, is calculated
    '''

    # Media Path of Nginx is solely MEDIA, this one here is /code/media

    path = os.path.join("/code"+path)
    print(path)
    if os.path.exists(path):
        print(path)
        new_path = move_upload_to_storage(path, name, creator, locker)
        print(new_path)
        image = BioImage.objects.create(file=new_path,
                                        creator_id=creator,
                                        locker_id=locker,
                                        name=os.path.basename(new_path))

        image.save()
        return image



        