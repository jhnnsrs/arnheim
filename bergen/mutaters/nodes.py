from drawing.models import LineROI
from elements.nodes import WatcherType
from larvik.discover import register_node, NodeType
from metamorphers.models import Display, Exhibit
from mutaters.models import Reflection


@register_node("reflectionshow")
class ReflectionShow(NodeType):
    inputs = [Reflection]
    type = "show"
    settings = {"reload": True}
    name = "Reflection"
    path = "ReflectionShow"

@register_node("watcher-reflection")
class ReflectionWatcher(WatcherType):
    inputs = []
    outputs = [Reflection]
    settings = {"reload": True}
    name = "Reflection Watcher"
    path = "ReflectionWatcher"
