import xarray
import zarr
from zarr import blosc

compressor = blosc.Blosc(cname='zstd', clevel=3, shuffle=blosc.Blosc.BITSHUFFLE)
blosc.use_threads = True

zarr.storage.default_compressor = compressor


def getStore(store):
    return zarr.DirectoryStore(store)

def getSynchronizer(store):
    return zarr.ProcessSynchronizer(f'{store}.sync')


def openDataset(store, group, chunks="auto") -> xarray.Dataset:
    storei = getStore(store)
    array =  xarray.open_zarr(store=storei, group=group)
    return array
