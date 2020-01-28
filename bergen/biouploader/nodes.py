from biouploader.models import BioImage, Locker, BioSeries
from elements.nodes import WatcherType, CollectorType
from larvik.discover import register_node, NodeType


@register_node("watcher-locker")
class LockerWatcherNode(WatcherType):
    inputs = []
    outputs = [Locker]
    name = "Locker Watcher"
    path = "LockerWatcher"
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
