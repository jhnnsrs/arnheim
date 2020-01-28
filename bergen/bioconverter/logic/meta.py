
import bioformats
from bs4 import BeautifulSoup



def parseMeta(meta,tree):


    results = {}

    for treekey, treevalue in tree.items():


        # If it is just a single item with Information
        if treevalue["type"] == "single":
            results[treekey] = {}
            el = meta.find(treevalue["key"])
            if el:
                for key, value in treevalue["values"].items():
                    try:
                        results[treekey][key] = value(el[key])
                    except:
                        results[treekey][key] = None

        # If it is just a single item with Information
        if treevalue["type"] == "multiple":
            results[treekey] = []
            els = meta.findAll(treevalue["key"])
            for index, el in enumerate(els):
                item = {}
                for key, value in treevalue["values"].items():
                    try:
                        item[key] = value(el[key])
                    except Exception as e:
                        item[key] = None



                results[treekey].append(item)

    return results


def loadBioMetaFromFile(filepath):
    unparsed = bioformats.get_omexml_metadata(filepath)
    return BeautifulSoup(unparsed, "xml")


def getSeriesNamesForFile(filepath):
    meta = loadBioMetaFromFile(filepath)
    allmeta = meta.findAll("Image")

    serieslist = []
    for series in allmeta:
        serieslist.append(series.attrs["Name"])

    return serieslist