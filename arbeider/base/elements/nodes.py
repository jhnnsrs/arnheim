from elements.models import ROI, Sample
from larvik.discover import register_node, NodeType

class SelectorType(NodeType):
    type = "selector"

class CollectorType(NodeType):
    type = "collector"

class WatcherType(NodeType):
    type = "watcher"

class IteratorType(NodeType):
    type = "iterator"

class FilterType(NodeType):
    type = "filter"


@register_node("rep-selector")
class RepresentationSelector(SelectorType):
    inputs = ["Locker", "Sample", "Roi"]
    outputs = ["Representation"]
    name = "RepresentationSelector"
    path = "RepresentationSelector"
    settings = {"rescale": True}

@register_node("watcher-roi")
class RoiWatcher(WatcherType):
    inputs = []
    outputs = [ROI]
    name = "ROI Watcher"
    path = "RoiWatcher"
    settings = {"rescale": True}


@register_node("watcher-sample")
class SampleWatcher(WatcherType):
    inputs = []
    outputs = [Sample]
    name = "Sample Watcher"
    path = "SampleWatcher"
    settings = {"rescale": True}

@register_node("impulsor")
class Impulsor(NodeType):
    type= "impulsor"
    inputs = ["*"]
    outputs = ["Impuls"]
    name = "Impulsor    "
    path = "Impulsor"
    settings = {"rescale": True}

