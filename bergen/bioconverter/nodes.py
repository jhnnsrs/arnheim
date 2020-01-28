from bioconverter.models import Representation
from biouploader.models import BioImage, Locker
from elements.nodes import WatcherType, SelectorType
from larvik.discover import register_node, NodeType

class Channel:
    pass



@register_node("watcher-rep")
class RepresentationWatcherNode(WatcherType):
    inputs = []
    outputs = [Representation]
    name = "Representation Watcher"
    path = "RepresentationWatcher"
    settings = {"rescale": True}



@register_node("selector-channel")
class RepresentationWatcherNode(SelectorType):
    inputs = [Representation]
    outputs = [Channel]
    name = "Channel Selector"
    path = "ChannelSelector"
    settings = {"rescale": True}
