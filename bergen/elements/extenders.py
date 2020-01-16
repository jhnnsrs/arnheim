import xarray as xr
import pandas as pd
import dask.array as da

from larvik.logging import get_module_logger

logger = get_module_logger(__name__)

logger.info("Making DataArrays Look Beautiful")

xr.set_options(display_style="html")
logger.info("Extending DataArray")
@xr.register_dataarray_accessor("biometa")
class MetaAccessor:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        self._channelvalue = None
        self._channeldict = None
        self._planesdict = None
        self._planes = None

    @property
    def channels(self):
        """Return the geographic center point of this dataset."""
        # we can use a cache on our accessor objects, because accessors
        # themselves are cached on instances that access them.
        self._channeldict = {}
        try:
            for item in self._obj.attrs["channels"]:
                self._channeldict[item["Name"]] = item
        except KeyError:
            raise NotImplementedError("The Array you are interfacing with is not an Arnheim array with the required Biometa Attributes")

        try:
            values = [self._channeldict[str(value)] for value in self._obj.channel.values]
        except TypeError as e:
            values = [self._channeldict[str(self._obj.channel.values)]]

        return pd.DataFrame(values)

    @property
    def scan(self):
        """Return the geographic center point of this dataset."""
        return pd.DataFrame(self._obj.attrs["scan"])

    @property
    def planes(self):
        """Return the planes of this Xarray."""
        # we can use a cache on our accessor objects, because accessors
        # themselves are cached on instances that access them.

        if self._planesdict is None:
            self._planesdict = {}
            try:
                for item in self._obj.attrs["planes"]:
                    self._planesdict[item["TheZ"]] = item
            except KeyError:
                raise NotImplementedError("The Array you are interfacing with is not an Arnheim array with the required Biometa Attributes")
        try:
            values = [self._planesdict[str(value)] for value in self._obj.z.values]
        except TypeError as e:
            values = [self._planesdict[str(self._obj.z.values)]]
        except KeyError as e:
            raise NotImplementedError("This X-Array does not containt a Z-Axis")

        self._planevalues = values
        return pd.DataFrame(self._planevalues)


@xr.register_dataarray_accessor("helpers")
class HelperAccesor:
    def __init__(self, xarray_obj):
        self._obj: xr.DataArray = xarray_obj
        self._channelvalue = None
        self._channeldict = None
        self._planesdict = None
        self._planes = None

    def appendChannel(self, size=1, name=None, dim="channel", constructor=da.zeros, tosize=None):
        """Return the geographic center point of this dataset."""
        if name is None:
            name = f'empty-{dim}'
        newshape = list(self._obj.shape)
        oldsize = newshape[self._obj.dims.index(dim)]
        if (oldsize >= tosize): return self._obj
        if tosize is not None: size = tosize - oldsize
        if tosize is not None:
            newshape[self._obj.dims.index(dim)] = size
        else:
            newshape[self._obj.dims.index(dim)] = size
        for i in range(size):
            self._obj.attrs["channels"].append({"Type": "Fake Zeros", "Name": f"{name}-{i}"})
        # we can use a cache on our accessor objects, because accessors
        # themselves are cached on instances that access them.
        zeros = xr.DataArray(constructor(newshape), dims=["x","y","channel","time"], coords={**self._obj.coords, dim:[f"{name}-{x}" for x in range(size)]}, name=self._obj.name, attrs=self._obj.attrs)
        return xr.concat([self._obj,zeros],dim=dim)

