import xarray
from dask.bag import Bag
from django.db.models.query import QuerySet
import dask.bag as db
import dask.dataframe as dd
from dask.bag.core import Bag

from larvik.helpers import LarvikManager


class BioMetaAccesor(object):

    def __init__(self, bag):
        self.bag = bag

    @property
    def channels(self):
        def get_biometa(array):
            df = dd.from_dask_array(array.channels.data)
            df["Array"] = array.name
            return df

        datasets = self.bag.map(get_biometa)
        return datasets.fold(lambda x,y: dd.concat([x,y]))


class LarvikBag(object):

    def __init__(self, bag, *args, **kwargs):
        self.bag = bag
        self._biometa = None
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

    @property
    def biometa(self):
        if not self._biometa:
            self._biometa = BioMetaAccesor(self.bag)
        return self._biometa

    def __repr__(self):
        return self.bag.__repr__()

class LarvikArrayQueryset(QuerySet):

    def delete(self):
        for el in self.all():
            el.zarr.delete()


    def spread(self):

        arrayslist = []
        for el in self.all():
            arrayslist.append(el.store.load())

        return LarvikBag(db.from_sequence(arrayslist))

    def asDataset(self, **kwargs):
        return xarray.merge(self.spread().bag, **kwargs)