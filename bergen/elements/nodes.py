from larvik.discover import register_node, NodeType

class SelectorType(NodeType):
    type = "selector"

class CollectorType(NodeType):
    type = "collector"

class WatcherType(NodeType):
    type = "watcher"



@register_node("rep-selector")
class RepresentationSelector(SelectorType):
    inputs = ["Locker", "Sample", "Roi"]
    outputs = ["Representation"]
    name = "RepresentationSelector"
    path = "RepresentationSelector"
    settings = {"rescale": True}


