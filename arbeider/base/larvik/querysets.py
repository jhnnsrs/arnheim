import xarray
from dask.bag import Bag
from django.db.models.query import QuerySet
import dask.bag as db
from dask.bag.core import Bag

from larvik.helpers import LarvikManager
from larvik.storage.store import openDataset


class LarvikBag(object):

    def __init__(self, bag, *args, **kwargs):
        self.bag = bag
        self.settings = {}

    def __getattr__(self, item):
        func = getattr(self.bag, item)
        def inner(*args, **kwargs):
            value = func(*args, **kwargs)
            if isinstance(value, Bag):
                return LarvikBag(value)
            else:
                return value

        return inner

    def parseSettings(self,settings):
        self.settings = settings

    def parse(self, *args):
        ''' :param *args Array of ParserSubclass'''
        parsedb = self.bag
        manager = LarvikManager()

        for i, parser in enumerate(args):
            parsedb = parsedb.map(parser.filter, self.settings, manager)

        return LarvikBag(parsedb)

    def __repr__(self):
        return self.bag.__repr__()

class LarvikArrayQueryset(QuerySet):


    def asBag(self):

        def toarray(params) -> xarray.DataArray:
            xr = openDataset(params["zarr__store"], params["zarr__group"])["data"]
            xr.name = params["name"]
            return xr

        b = db.from_sequence(list(self.values("name","zarr__store","zarr__group")), partition_size=1)
        return LarvikBag(b.map(toarray))

    def asDataset(self, **kwargs):
        return xarray.merge(self.asBag().bag, **kwargs)