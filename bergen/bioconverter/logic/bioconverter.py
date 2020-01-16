import javabridge
import numpy as np
import dask.array as da
import xarray as xr
import zarr as zr
import bioformats
import logging
import json
import pandas as pd
from django.conf import settings

from bioconverter.logic.bioparser import loadBioMetaFromFile

javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)

BITMAP = {
    "uint8": 8,
    "uint16": 16,
    "uint32": 32,
}

DESIRED_DTYPE = settings.ZARR_DTYPE


def parseSoup(soup, df_cols, items=None):
    """Parse the input XML file and store the result in a pandas
    DataFrame with the given columns.

    The first element of df_cols is supposed to be the identifier
    variable, which is an attribute of each node element in the
    XML data; other features will be parsed from the text content
    of each sub-element.
    """
    tr = soup
    channels = tr.findAll(items) if items else tr
    l = []
    for channel in channels:
        row = []
        for item in df_cols:
            try:
                row.append(channel[item])
            except KeyError as e:
                row.append(None)
        l.append(row)
    return pd.DataFrame(l, columns=df_cols)


def getChannels(biometa):
    return {"channels": parseSoup(biometa,["Name", "EmissionWavelength", "ExcitationWavelength",
                              "IlluminationType", "AcquisitionMode","Color", "SamplesPerPixel"], items="Channel")}


def getPlanes(biometa):
    return {"planes": parseSoup(biometa,["PositionZ", "TheZ", "TheC", "TheT""ExposureTime", "DeltaT", "PositionZUnit", "PositionX",
                      "PositionY"], items="Plane")}


def getShape(biometa):
    shapelist = parseSoup(biometa, ["SizeX", "SizeY", "SizeC", "SizeZ", "SizeT"], items="Pixels")
    shape = shapelist.values.tolist()[0]
    print(shape)
    return {"shape": [int(item) for item in shape]}


def getScan(biometa):
    return { "scan": parseSoup(biometa, ["SizeX", "SizeY", "SizeC", "SizeZ", "SizeT",
                               "PhysicalSizeX", "PhysicalSizeY", "PhysicalSizeZ",
                               "PhysicalSizeXUnit", "PhysicalSizeYUnit", "PhysicalSizeZUnit",
                               "SignificantBits", "Type",

                               ], items="Pixels")}


def getDate(biometa):
    try:
        return {"dates": pd.DataFrame(biometa.findAll("AcquisitionDate", text=True)[0].findAll(text=True),
                            columns=["AcquisitionDate"])}
    except:
        return {"dates":pd.DataFrame([None], columns=["AcquisitionDate"])}


def getProperties(biometa):
    detector = parseSoup(biometa, ["Model", "Type"], items="Detector")
    objective = parseSoup(biometa, ["RefractiveIndex", "Medium"], items="ObjectiveSettings")

    return {"objective": objective, "detector": detector}


def constructMeta(biometa):
    print("HALLO")

    return {**getScan(biometa),
        **getDate(biometa),
        **getShape(biometa),
        **getProperties(biometa),
        **getChannels(biometa),
        **getPlanes(biometa)}

async def constructParsing(filepath, index, progress):
    print("HALLO")
    parsing = {"filepath": filepath, "index": index}

    filemeta= loadBioMetaFromFile(filepath)
    biometa = filemeta.metadata.findAll("Image")[index]
    await progress("Constructing Parsing")

    return {**parsing, **constructMeta(biometa)}

async def loadArrayFromTest(test, progress):
    filepath = test["filepath"]
    shape = test["shape"]
    print(shape)
    channeldict = {}
    channels = test["channels"].to_dict(orient='records')
    planes = test["planes"].to_dict(orient="records")
    imagesettings = test["scan"].to_dict(orient="records")  # there is only on setting

    settings = imagesettings[0]
    channelnames = [item["Name"] for item in channels]

    newfile = xr.DataArray(np.zeros(shape, dtype=DESIRED_DTYPE), dims=["x", "y", "channel", "z", "time"],)
    newfile = xr.DataArray(newfile, coords={"physx": newfile.x * float(settings["PhysicalSizeX"]),
                                            "physy": newfile.y * float(settings["PhysicalSizeY"]),
                                            "phsyz": newfile.z * float(settings["PhysicalSizeZ"]),
                                            "x": newfile.x,
                                            "y": newfile.y,
                                            "z": newfile.z,
                                            "time": newfile.time,
                                            "channel": channelnames
                                            })

    # TODO: Better bitconversion and Decission, ALSO BIG ENDIAN NOTATION

    inputtype = settings.get("Type")
    bitness = BITMAP.get(inputtype)
    if "SignificantBits" in settings:
        leastsig = int(settings.get("SignificantBits"))
        await progress("This Sample needs rescaling because of Unsignificant Bits")
        significantfactor = 2 ** bitness // 2 ** leastsig
    else:
        significantfactor = 1

    if DESIRED_DTYPE == "float64":
        #This means we actually want to imagereader to rescale the data and just adjsut for significant bits
        rescale = True
        scalefactor  = significantfactor
    else:
        rescale = False
        inputbits = BITMAP.get(inputtype)
        outputbits = BITMAP.get(DESIRED_DTYPE)

        scalefactor = significantfactor * 2 ** outputbits // 2 ** inputbits


    try:
        # loads a cached reader that reads every frame
        with bioformats.ImageReader(filepath, perform_init=True) as reader:
            for c in range(shape[2]):
                await progress(f"Parsing Channel {c}")
                for z in range(shape[3]):
                    for t in range(shape[4]):

                        # bioformats appears to swap axes for tif images and read all three channels at a time for RGB
                        im1 = reader.read(c=c, z=z, t=t, series=test["index"], rescale=rescale, channel_names=None)
                        if scalefactor != 1:
                            im1 = im1 * scalefactor #Bitwise scaling because of weird bioformats rescaling issuess
                        if im1.ndim == 3:
                            if im1.shape[2] == 3:
                                # Three channels are red
                                im2 = im1[:, :, c]
                            else:
                                im2 = im1
                        else:
                            im2 = im1
                        if (shape[0] == im2.shape[1]) and (shape[1] == im2.shape[0]) and not shape[0] == shape[1]:
                            # x and y are swapped
                            logging.warning("Image might be transposed. Swapping X and Y")
                            im3 = im2.transpose()
                        else:
                            im3 = im2

                        newfile[:, :, c, z, t] = im3

        logging.info("BioImage Parsed")
    finally:
        bioformats.clear_image_reader_cache()

    newfile.attrs["channels"] = channels
    newfile.attrs["planes"] = planes
    newfile.attrs["scan"] = imagesettings
    return newfile


async def getStack(parsing, progress):
    return await loadArrayFromTest(parsing,progress)