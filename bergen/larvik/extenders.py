import pandas as pd
import xarray as xr

from larvik.logging import get_module_logger
from mandal.settings import arnheim_debug

logger = get_module_logger(__name__)

if arnheim_debug:
    logger.info("Making DataArrays Look Beautiful")
    logger.info("Extending DataArray")

xr.set_options(display_style="html")


class ArnheimError(Exception):
    pass


@xr.register_dataarray_accessor("biometa")
class MetaAccessor:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        self._channelvalue = None
        self._channeldict = None
        self._planesdict = None
        self._planes = None

    def selchannel(self, **kwargs):
        """Return the geographic center point of this dataset."""
        # we can use a cache on our accessor objects, because accessors
        # themselves are cached on instances that access them.

        lala = pd.DataFrame(self._obj.channel.data.compute())
        for key, value in kwargs.items():
            lala = lala[lala[key] == value]

        return lala

    @property
    def name(self):
        return self._obj.attrs["seriesname"]

    @property
    def scan(self):
        return pd.DataFrame(self._obj.attrs["scan"])

    @property
    def channels(self):
        if not "channels" in self._obj.coords:
            raise ArnheimError("No channels. Did you transform the Array in (c) with coordinate changes?")
        """Return the geographic center point of this dataset."""
        # we can use a cache on our accessor objects, because accessors
        # themselves are cached on instances that access them.
        lala = pd.DataFrame(self._obj.channels.data.compute())
        return lala

    @property
    def planes(self):
        if not "planes" in self._obj.coords:
            raise ArnheimError("No planes. Did you transform the Array in (c,z,t) with coordinate changes?")
        """Return the geographic center point of this dataset."""
        # we can use a cache on our accessor objects, because accessors
        # themselves are cached on instances that access them.
        lala = pd.DataFrame(self._obj.planes.data.flatten().compute())
        return lala

    @property
    def savecoords(self):
        ''' All the save coordinates for accessing'''
        return [key for key, value in self._obj.coords.items()]


@xr.register_dataarray_accessor("viewer")
class MetaAccessor:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        self.log = logger.info

    def show(self, maxisp=True, t=0, rgb=(0, 1, 2)):
        image = self._obj
        if "t" in image.coords:
            self.log(f"Stack has {len(image.t)} Timepoints: selecting t={t}")
            image = image.sel(t=t)
        if "z" in image.coords and maxisp:
            self.log(f"Stack has {len(image.z)} Z Planes: Projecting maximum intensity")
            image = image.max(dim="z")

        if "c" in image.coords:
            if len(image.c) > 3:
                image = image.sel(c=rgb)
            if len(image.c) == 1:
                image = image.sel(c=image.c[0])
                return image.plot.imshow()
            return image.plot.imshow(rgb="c")
        else:
            return image.plot.imshow()
