from django.contrib import admin

# Register your models here.
from bioconverter.models import Converter, Conversing

admin.site.register(Converter)
admin.site.register(Conversing)