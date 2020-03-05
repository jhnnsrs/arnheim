from elements.models import ROI
from elements.nodes import WatcherType
from larvik.discover import register_node, NodeType
from metamorphers.models import Display, Exhibit


@register_node("twodshow")
class TwoDShow(NodeType):
    inputs = [Display]
    outputs = [ROI]
    type = "show"
    settings = {"reload": True}
    name = "Two D Show"
    path = "TwoDShow"


@register_node("watcher-display")
class DisplayWatcher(WatcherType):
    inputs = []
    outputs = [Display]
    settings = {"reload": True}
    name = "Display Watcher"
    path = "DisplayWatcher"

@register_node("watcher-exhibit")
class ExhibitWatcher(WatcherType):
    inputs = []
    outputs = [Exhibit]
    name = "Exhibit Watcher"
    path = "ExhibitWatcher"
    settings = {"rescale": True}