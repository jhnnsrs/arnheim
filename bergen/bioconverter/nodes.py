from bioconverter.models import Representation
from biouploader.models import BioSeries
from elements.models import Channel
from elements.nodes import WatcherType, SelectorType, FilterType
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
