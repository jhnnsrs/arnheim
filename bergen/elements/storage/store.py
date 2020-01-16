import xarray
import zarr


def getStore(store):
    from zarr import blosc
    compressor = blosc.Blosc(cname='zstd', clevel=3, shuffle=blosc.Blosc.BITSHUFFLE)
    blosc.use_threads = False

    zarr.storage.default_compressor = compressor
    return zarr.DirectoryStore(store)

def getSynchronizer(store):
    return zarr.ProcessSynchronizer(f'{store}.sync')


def openDataset(store, group, chunks="auto") -> xarray.Dataset:
    storei = getStore(store)
    return xarray.open_zarr(store=storei, group=group, chunks=chunks)
