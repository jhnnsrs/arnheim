import xarray
import zarr

from mandal.settings import ZARR_COMPRESSION


def getStore(store):
    from numcodecs import Blosc, LZMA
    if ZARR_COMPRESSION == None:
        compressor = Blosc(cname='zstd', clevel=3, shuffle=Blosc.BITSHUFFLE)
    else:
        compressor = LZMA()

    zarr.storage.default_compressor = compressor
    return zarr.DirectoryStore(store)


def openDataset(store, group, chunks="auto") -> xarray.Dataset:
    store = getStore(store)
    return xarray.open_zarr(store=store, group=group, chunks=chunks)