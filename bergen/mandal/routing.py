from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.urls import path

from answers.consumers import PandaAnswer
from bioconverter.consumers import BioConverter, ConvertBioSeriesOsloJob
from biouploader.consumers import BioAnalyzer
from evaluators.consumers import AISDataConsumer, ClusterDataConsumer
from filterbank.consumers import MaxISP, PrewittFilter, SlicedMaxISP, Mapping
from importer.consumers import Importer
from metamorphers.consumers import NiftiMetamorpher, ImageMetamorpher
from mutaters.consumers import ImageMutator
from revamper.consumers import MaskingRevamper
from transformers.consumers import LineRectifierTransformer, SliceLineTransformer
from trontheim.consumers import OsloConsumer
from trontheim.middleware import QueryAuthMiddleware
from visualizers.consumers import Profiler, ExcelExporter

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
        # PROCESSING PORTION

        # Importers (Files out)
        "importer": Importer,

        # Analyzers (File in Meta out)
        "analyzer": BioAnalyzer,

        # Converters (File in Rep and Sample Out)
        "bioconverter": BioConverter,
        "test": ConvertBioSeriesOsloJob,

        #Filters (Rep in Rep out)
        "maxisp": MaxISP,
        "slicedmaxisp": SlicedMaxISP,
        "mapping": Mapping,
        "prewitt": PrewittFilter,

        #Transformers (Rep, Roi, in Trans out)
        "linerect": LineRectifierTransformer,
        "sliceline": SliceLineTransformer,

        # Revampers (Transin, Transout -> like Filter)
        "masker": MaskingRevamper,

        # Evaluators
        "aisdata": AISDataConsumer,
        "clusterdata": ClusterDataConsumer,


        # VISUALIZATION PART

        #Metamorphers ( Rep in Visual out)
        "nifti": NiftiMetamorpher,
        "image": ImageMetamorpher,


        #Mutaters (Trans in Visual out)
        "transformimage": ImageMutator,






        #DATA PORTION
        #Oracles
        "pandas": PandaAnswer,

        #Visualizers
        "profiler": Profiler,
        "excelexport": ExcelExporter,

    }),
})
