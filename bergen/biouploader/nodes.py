from biouploader.models import BioImage, Locker, BioSeries
from elements.models import Impuls
from elements.nodes import WatcherType, CollectorType, IteratorType
from larvik.discover import register_node


@register_node("watcher-locker")
class LockerWatcherNode(WatcherType):
    inputs = []
    outputs = [Locker]
    name = "Locker Watcher"
    path = "LockerWatcher"
    settings = {"rescale": True}


@register_node("iterator-locker")
class LockerIteratorNode(IteratorType):
    inputs = [Locker, Impuls]
    outputs = [BioImage]
    name = "Locker Iterator"
    path = "LockerIterator"
    settings = {"rescale": True}




@register_node("watcher-bioimage")
class BioImageWatcher(WatcherType):
    inputs = []
    outputs = [BioImage]
    name = "Bioimage Watcher"
    path = "BioImageWatcher"
    settings = {"rescale": True}

@register_node("collecor-bioseries")
class BioSeriesCollector(CollectorType):
    inputs = [BioSeries]
    outputs = [BioSeries]
    name = "BioSeriesCollectorr"
    path = "BioSeriesCollector"
    settings = {"rescale": True}

