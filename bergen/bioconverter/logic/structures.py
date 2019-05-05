

class BioMetaStructure(object):
    def __init__(self, standalone=True, series=0):

        self.valid = False
        self.standalone = standalone
        self.date = 0
        self.sizex = 0
        self.sizey = 0
        self.sizez = 0
        self.frames = 0
        self.sizet = 0
        self.sizec = 3
        self.series = series
        self.shape = None
        self.metadata = None
        self.unparsed = ""

        # self.physicalsizet = float(image.find("Pixels").attrs[""])
        self.physicalsizex = 1
        self.physicalsizey = 1
        self.physicalsizexunit = "mm"
        self.physicalsizeyunit = "mm"

        self.seriesname = None
        self.channellist = None
        self.dirname = None
        self.filename = None

    def __str__(self):
        if self.filename:
            str("BioMeta of file {}".format(self.filename))
        else:
            str("Unparsed BioMeta. Please parse first (logic.loadBioMetaSeriesFromFile)")


class BioImage:

    def __init__(self):
        self.filepath = None
        self.layer = None
        self.channels = None
        self.c = None

        # STANDARD SETTINGS HERE
        self.debug = None
        self.series = 0
        self.setz = 0

        # META
        self.shape = (0, 0, 0)

        # DATA
        self.file = None

    def __str__(self):
        return self.filepath