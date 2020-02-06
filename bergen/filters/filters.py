import dask.array as da
import dask_image.ndfilters
import xarray as xr
from larvik.helpers import LarvikParser, LarvikManager


class MaxISP(LarvikParser):

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager) -> xr.DataArray:
        manager.progress("Done")
        return array.max(axis=3, keep_attrs=True)


class SlicedMaxISP(LarvikParser):

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager) -> xr.DataArray:
        lowerBound: int = int(settings.get("lowerBound", -1))
        upperBound: int = int(settings.get("upperBound", -1))

        array = array.sel(z=slice(lowerBound, upperBound)).max(dim="z")

        return array


class Prewitt(LarvikParser):

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager: LarvikManager) -> xr.DataArray:
        it = array
        prewx = dask_image.ndfilters.prewitt(it.data, axis=0)
        prewy = dask_image.ndfilters.prewitt(it.data, axis=1)

        prewittfiltered = da.sqrt(prewx * prewx + prewy * prewy)
        manager.progress("Hallo")
        c = manager.meta.prepend(it, string="Prewitt of")
        channels = xr.DataArray(da.array(c), dims="c")

        x = xr.DataArray(prewittfiltered, dims=it.dims, coords={ **it.coords, "channels": channels})
        manager.progress("Hallo")
        return x


class Mapping(LarvikParser):

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager) -> xr.DataArray:
        threed = array

        rchannel = threed.sel(c=[1, 0])
        gchannel = threed.sel(c=[1, 0])
        bchannel = threed.sel(c=[0])

        rmeta = manager.meta.merge([1, 0], threed)
        gmeta = manager.meta.merge([1, 0], threed)
        bmeta = manager.meta.merge([0], threed)

        channels = xr.DataArray(da.from_array([rmeta, gmeta, bmeta]), dims=["c"])

        r = rchannel.max(dim="c", keepdims=True)
        g = gchannel.max(dim="c", keepdims=True)
        b = bchannel.max(dim="c", keepdims=True)

        x = da.concatenate([r.data, g.data, b.data], axis=2)
        x = xr.DataArray(x, dims=threed.dims, coords={**threed.coords, "channels": channels, "c": range(3)})

        return x

