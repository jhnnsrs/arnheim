import xarray as xr
import bioformats
import dask.array as da
import xarray as xr
import numpy as np

from bioconverter.logic.meta import loadBioMetaFromFile, parseMeta
from bioconverter.logic.ome import imagetree
from bioconverter.logic.utils import constructDim, calculateRescaleAndScaleFactor


async def convertBioImageToXArray(filepath, index, progress):
    await progress("Loading Biometa")
    biometa = loadBioMetaFromFile(filepath)
    imagemeta = biometa.findAll("Image")[index]

    # General Parsing Parameters
    name = imagemeta.attrs["Name"]
    parsedimagemeta = parseMeta(imagemeta, imagetree)
    scan = parsedimagemeta["scan"]
    shape = (scan["SizeX"], scan["SizeY"], scan["SizeC"], scan["SizeZ"], scan["SizeT"])

    # Channels and Planes (TODO: Planes are given to be in z,c,t shape in xml format?, if error: sort)
    zlinearorderedplanes = constructDim(imagetree, parsedimagemeta, "planes", "z")
    zctorderplanes = zlinearorderedplanes.data.reshape((scan["SizeZ"], scan["SizeC"], scan["SizeT"]))

    channels = constructDim(imagetree, parsedimagemeta, "channels", "c")
    planes = xr.DataArray(zctorderplanes, dims=("z", "c", "t"))

    rescale, scalefactor = await calculateRescaleAndScaleFactor(scan, progress)
    if rescale: await progress(f"Rescaling because we want float64")
    await progress(f"Insignificant Bits detected: Scalefactor of {scalefactor}x applies")
    # Population
    newfile = da.zeros(shape)
    newfile = xr.DataArray(newfile, dims=["x", "y", "c", "z", "t"])
    newfile = xr.DataArray(newfile, coords={"physx": newfile.x * float(scan["PhysicalSizeX"]),
                                            "physy": newfile.y * float(scan["PhysicalSizeY"]),
                                            "phsyz": newfile.z * float(scan["PhysicalSizeZ"]),
                                            "physt": newfile.t * float(
                                                scan.get("TimeIncrement", 1) if scan.get("TimeIncrement",
                                                                                         1) is not None else 1),
                                            "x": newfile.x,
                                            "y": newfile.y,
                                            "z": newfile.z,
                                            "t": newfile.t,
                                            "c": newfile.c,
                                            "channels": channels,
                                            "planes": planes
                                            })

    try:
        # loads a cached reader that reads every frame
        with bioformats.ImageReader(filepath, perform_init=True) as reader:
            for c in range(shape[2]):
                await progress(f"Processing channel {channels[c].data['Name']}")
                for z in range(shape[3]):
                    for t in range(shape[4]):

                        # bioformats appears to swap axes for tif images and read all three channels at a time for RGB
                        im1 = reader.read(c=c, z=z, t=t, series=index, rescale=rescale, channel_names=None)
                        if scalefactor != 1:
                            im1 = im1 * scalefactor
                        if im1.ndim == 3:
                            if im1.shape[2] == 3:
                                # Three channels are red
                                im2 = im1[:, :, c]
                            else:
                                im2 = im1
                        else:
                            im2 = im1
                        if im2.shape[0] == shape[1] and im2.shape[0] != shape[0]:
                            # Transposed axes for whatever reason
                            im3 = np.swapaxes(im2, 0, 1)
                        else:
                            im3 = im2

                        newfile[:, :, c, z, t] = im3

        await progress("BioImage Parsed")
    finally:
        bioformats.clear_image_reader_cache()

    newfile.attrs["scan"] = [scan]
    newfile.attrs["seriesname"] = name

    newfile.name = name

    return newfile, parsedimagemeta
