from django.contrib import admin

# Register your models here.
from flow.models import Flow, Node, Layout, External, ExternalRequest

admin.site.register(Flow)
admin.site.register(Node)
admin.site.register(Layout)
admin.site.register(External)
admin.site.register(ExternalRequest)