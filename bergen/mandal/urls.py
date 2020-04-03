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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from rest_framework import routers
from rest_framework.schemas import get_schema_view


import answers.routes
import bioconverter.routes
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


# Rest Framework Routers
router = routers.DefaultRouter()
router.registry.extend(social.routes.router.registry)
router.registry.extend(drawing.routes.router.registry)
router.registry.extend(elements.routes.router.registry)
router.registry.extend(filters.routes.router.registry)
router.registry.extend(bioconverter.routes.router.registry)
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


# Bootstrap Backend
@login_required
def index(request):
        # Render that in the index template
    return render(request, "index-oslo.html")



urlpatterns = [
    path('', index, name='index'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^graphql$', GraphQLView.as_view(graphiql=True)),
    path('admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include((router.urls, 'api'))),
    path('openapi', get_schema_view(
            title="Arnheim",
            description="API for accessing the underlying Architecture",
            version="1.0.0"
        ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(
            template_name='redoc.html',
            extra_context={'schema_url':'openapi-schema'}
        ), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

