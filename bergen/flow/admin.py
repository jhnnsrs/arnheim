from django.contrib import admin

# Register your models here.
from flow.models import Flow, ConversionFlow, FilterFlow

admin.site.register(Flow)
admin.site.register(FilterFlow)
admin.site.register(ConversionFlow)