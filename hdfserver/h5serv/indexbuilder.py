import sys
import h5py
import logging
from h5json import Hdf5db
import copy
# setup logger
log = logging.getLogger("rebuildIndex")
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
# create formatter
formatter = logging.Formatter("%(levelname)s:%(filename)s:%(lineno)d::%(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate = False

lastfile = None
lastlength = None
breakpoint = False
dbname = "__db__"

def rebuild_index(filepath):
    # remove the old index
    global lastfile, lastlength, breakpoint

    if breakpoint:
        breakpoint = False
        return


    file = h5py.File(filepath, 'a')
    if dbname in file:
        # if db is actually the same as before just return without updating
        length = len(file[dbname]["{datasets}"].attrs)
        log.info(length)
        if length == lastlength and lastfile == filepath:
            log.info("File is the fucking same, we do not care")
            breakpoint = True
            return

        length = lastlength

        log.info("deleting old db group")
        del file[dbname]

    file.close()

    log.info("reached here")
    # now open with hdf5db

    with Hdf5db(filepath, app_logger=log) as db:
        # the actual index rebuilding will happen in the init function
        root_uuid = db.getUUIDByPath('/')
        print("root_uuid:", root_uuid)

    file = h5py.File(filepath, 'a')
    if dbname in file:
        # if db is actually the same as before just return without updating
        lastlength = len(file[dbname]["{datasets}"].attrs)
        log.info("New Length",str(lastlength))
        lastfile = filepath

    file.close()

    log.info("Done")