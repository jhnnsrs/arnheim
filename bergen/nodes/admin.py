from django.contrib import admin

# Register your models here.
from nodes.models import Node

admin.site.register(Node)