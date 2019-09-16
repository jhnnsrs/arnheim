from django.contrib import admin

# Register your models here.
from nodes.models import Node, Layout

admin.site.register(Node)
admin.site.register(Layout)