from elements.models import ROI
from larvik.discover import register_node, NodeType
from metamorphers.models import Display


@register_node("twodshow")
class TwoDShow(NodeType):
    inputs = [Display]
    outputs = [ROI]
    type = "show"
    settings = {"reload": True}
    name = "Two D Show"
    path = "TwoDShow"