from django.contrib import admin

# Register your models here.
from flow.models import Flow, Node, Layout

admin.site.register(Flow)
admin.site.register(Node)
admin.site.register(Layout)