import numpy as np
import xarray as xr
try:
    from django.conf import settings
except:
    class Settings(object):
        ZARR_DTYPE = "float64"
    settings = Settings()

DTYPEMAP = {
    "uint8": np.dtype("uint8"),
    "uint16": np.dtype("uint16"),
    "uint32": np.dtype("uint32"),
    "int16": np.dtype("int16"),
}

DESIRED_DTYPE = np.dtype(settings.ZARR_DTYPE)


def constructDim(tree, results, accesor, dim):
    channels = results[accesor]
    dtypedict = tree[accesor]["values"]
    values = []
    dt = []
    dims = []
    for i, channel in enumerate(channels):
        items = [i]
        keys = [("Index", np.dtype(int))]
        for key, value in channel.items():
            items.append(value)
            if dtypedict[key] == str:
                keys.append((key, "U250"))
            else:
                keys.append((key, dtypedict[key]))

        values.append(tuple(items))
        dt = keys

    lala = np.array(values, dtype=dt)
    return xr.DataArray(lala, dims=dim)


async def calculateRescaleAndScaleFactor(scan, progress):
    inputtype = scan.get("Type")
    dtype = DTYPEMAP.get(inputtype)
    bitness = dtype.alignment * 8

    await progress(f"Input dtype has {bitness} Bits")

    if "SignificantBits" in scan:
        # Bitwise scaling because of weird bioformats rescaling issuess
        leastsig = int(scan.get("SignificantBits") if scan.get("SignificantBits") else bitness)
        await progress(f"Input dtype has {leastsig} significant Bits")
        significantfactor = 2 ** bitness // 2 ** leastsig
    else:
        significantfactor = 1

    if DESIRED_DTYPE == np.float64 or DESIRED_DTYPE == np.dtype(float):
        # This means we actually want to imagereader to rescale the data and just adjsut for significant bits
        rescale = True
        scalefactor = significantfactor
    else:
        rescale = False
        outputbits = DESIRED_DTYPE.alignment * 8
        scalefactor = significantfactor * 2 ** outputbits // 2 ** bitness

    return rescale, scalefactor