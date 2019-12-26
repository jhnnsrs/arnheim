import os

from elements.models import Sample
from strainers.models import Straining
from mandal import settings
import zarr

def sampleToFilename(sample: Sample):
    return "sample-{0}.zarr".format(sample.id)

def strainingToVid(straining: Straining):
    type = "transformation"
    vidfirst = "transformation_transformation-{0}_strainer-{1}_node-{2}".format(str(straining.transformation_id),
                                                                                str(straining.strainer_id),
                                                                                str(straining.nodeid))

    return "{0}/{1}".format(type,vidfirst)

def writeOutputForStraining(straining: Straining, array):
    ''' Will create a Local Zarr Array and return the Instance '''
    vid = strainingToVid(straining)
    filename = sampleToFilename(straining.sample)
    filepath = os.path.join(settings.ZARR_ROOT,filename)
    z2 = zarr.open('filepath', mode='w', shape=(10000, 10000),chunks=(1000, 1000), dtype='i4')

    return z2