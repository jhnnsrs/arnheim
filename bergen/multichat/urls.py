from django.conf.urls import url
from django.urls import path, include, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

import drawing.routes
import elements.routes
import filterbank.routes
import metamorphers.routes
import mutaters.routes
import nodes.routes
import social.routes
import bioconverter.routes
import frontend.routes
import evaluators.routes
import biouploader.routes
import transformers.routes
import flow.routes
from biouploader.views import upload_complete
from chat.views import index, test
from representations.views import TagAutocomplete

router = routers.DefaultRouter()
router.registry.extend(social.routes.router.registry)
router.registry.extend(drawing.routes.router.registry)
router.registry.extend(elements.routes.router.registry)
router.registry.extend(filterbank.routes.router.registry)
router.registry.extend(bioconverter.routes.router.registry)
router.registry.extend(frontend.routes.router.registry)
router.registry.extend(biouploader.routes.router.registry)
router.registry.extend(metamorphers.routes.router.registry)
router.registry.extend(transformers.routes.router.registry)
router.registry.extend(evaluators.routes.router.registry)
router.registry.extend(mutaters.routes.router.registry)
router.registry.extend(flow.routes.router.registry)
router.registry.extend(nodes.routes.router.registry)


urlpatterns = [
    path('', index),
    path('trontheim', test),
    re_path(r'^uploaded?/$', upload_complete, name='upload_complete'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include((router.urls, 'api'))),
    url(r'^tags/$',TagAutocomplete.as_view(),name='tags'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
