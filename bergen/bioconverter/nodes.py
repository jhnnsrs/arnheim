from bioconverter.models import BioSeries, Locker, BioImage
from elements.models import Channel, Representation, Impuls
from elements.nodes import WatcherType, SelectorType, FilterType, CollectorType, IteratorType
from larvik.discover import register_node


@register_node("watcher-rep")
class RepresentationWatcherNode(WatcherType):
    inputs = []
    outputs = [Representation]
    name = "Representation Watcher"
    path = "RepresentationWatcher"
    settings = {"rescale": True}



@register_node("selector-channel")
class ChannelSelectorNode(SelectorType):
    inputs = [Representation]
    outputs = [Channel]
    name = "Channel Selector"
    path = "ChannelSelector"
    settings = {"rescale": True}

@register_node("filter-bioseries")
class BioSeriesFilterNode(FilterType):
    inputs = [BioSeries]
    outputs = [BioSeries]
    name = "BioSeries Filter"
    path = "BioSeriesFilter"
    settings = {"rescale": True}

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