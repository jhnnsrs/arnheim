from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack

from bioconverter.consumers import BioConverter, ConvertBioSeriesOsloJob
from biouploader.consumers import BioAnalyzer
from evaluators.consumers import AISDataConsumer, ClusterDataConsumer
from filterbank.consumers import MaxISP, PrewittFilter, SlicedMaxISP, Mapping
from kafkaconsumers.kafkaconsumer import ChannelKafkaConsumer
from kafkaconsumers.parsers import Parsing
from metamorphers.consumers import NiftiMetamorpher, ImageMetamorpher
from mutaters.consumers import ImageMutator
from revamper.consumers import MaskingRevamper
from transformers.consumers import LineRectifierTransformer, SliceLineTransformer
from trontheim.middleware import QueryAuthMiddleware
from chat.consumers import ChatConsumer
from trontheim.consumers import OsloConsumer, OsloJobConsumer

OauthMiddleWareStack = lambda inner: QueryAuthMiddleware(AuthMiddlewareStack(inner))

# The channel routing defines what connections get handled by what consumers,
# selecting on either the connection type (ProtocolTypeRouter) or properties
# of the connection's scope (like URLRouter, which looks at scope["path"])
# For more, see http://channels.readthedocs.io/en/latest/topics/routing.html
application = ProtocolTypeRouter({

    # Channels will do this for you automatically. It's included here as an example.
    # "http": AsgiHandler,

    # Route all WebSocket requests to our custom chat handler.
    # We actually don't need the URLRouter here, but we've put it in for
    # illustration. Also note the inclusion of the AuthMiddlewareStack to
    # add users and sessions - see http://channels.readthedocs.io/en/latest/topics/authentication.html
    "websocket": QueryAuthMiddleware(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("oslo", OsloConsumer)
        ]),
    ),
    "channel": ChannelNameRouter({
        "maxisp": MaxISP,
        "slicedmaxisp": SlicedMaxISP,
        "mapping": Mapping,
        "prewitt": PrewittFilter,
        "bioconverter": BioConverter,
        "nifti": NiftiMetamorpher,
        "image": ImageMetamorpher,
        "test": ConvertBioSeriesOsloJob,
        "linerect": LineRectifierTransformer,
        "sliceline": SliceLineTransformer,
        "transformimage": ImageMutator,
        "aisdata": AISDataConsumer,
        "analyzer": BioAnalyzer,
        "kafka": Parsing,
        "kafkain": ChannelKafkaConsumer,
        "clusterdata": ClusterDataConsumer,
        "masker": MaskingRevamper
    }),
})
