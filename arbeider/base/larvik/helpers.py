import xarray as xr


class MetaMethods(object):

    def prepend(self, el, string= "Prewitt of"):
        items = el.channels.data.compute()
        for merge in items:
            merge["Name"] = f"{string} {merge['Name']}"
        return items

    def merge(self,channels: list, el):
        items = el.sel(c=channels).channels.data.compute()
        if len(items) == 1:
            return items[0]
        name = ",".join([item["Name"] for item in items])

        merge = items[0]
        merge["Index"] = -1
        merge["Name"] = f"Merged Channel ({name})"
        return merge



class LarvikManager(object):

    def __init__(self):
        self.meta = MetaMethods()
        self.iteration = None
        self.name = self.__class__.__name__

    @staticmethod
    def fromIteration(iteration, name):
        manager = LarvikManager()
        manager.iteration = iteration
        manager.name = name
        return manager

    def progress(self, progress):
        print(f"Iter {self.iteration} at {self.name}: {progress}")

    def persist(self, graph):
        graph.persist()

    def compute(self, graph):
        graph.compute()





class LarvikParser(object):

    @staticmethod
    def filter(array: xr.DataArray, settings: dict, manager: LarvikManager) -> xr.DataArray:
        raise NotImplementedError