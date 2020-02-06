"""mandal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from graphene_django.views import GraphQLView
from rest_framework import routers

import answers.routes
import bioconverter.routes
import biouploader.routes
import drawing.routes
import elements.routes
import evaluators.routes
import filters.routes
import flow.routes
import importer.routes
import metamorphers.routes
import mutaters.routes
import revamper.routes
import social.routes
import strainers.routes
import transformers.routes
import visualizers.routes
from biouploader.views import upload_complete
from chat.views import index, test

router = routers.DefaultRouter()
router.registry.extend(social.routes.router.registry)
router.registry.extend(drawing.routes.router.registry)
router.registry.extend(elements.routes.router.registry)
router.registry.extend(filters.routes.router.registry)
router.registry.extend(bioconverter.routes.router.registry)
router.registry.extend(biouploader.routes.router.registry)
router.registry.extend(metamorphers.routes.router.registry)
router.registry.extend(visualizers.routes.router.registry)
router.registry.extend(strainers.routes.router.registry)
router.registry.extend(importer.routes.router.registry)
router.registry.extend(answers.routes.router.registry)
router.registry.extend(transformers.routes.router.registry)
router.registry.extend(evaluators.routes.router.registry)
router.registry.extend(mutaters.routes.router.registry)
router.registry.extend(flow.routes.router.registry)
router.registry.extend(revamper.routes.router.registry)


urlpatterns = [
    path('', index, name='index'),
    path('trontheim', test),
    re_path(r'^uploaded?/$', upload_complete, name='upload_complete'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^graphql$', GraphQLView.as_view(graphiql=True)),
    path('admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include((router.urls, 'api'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

