from django.contrib import admin

# Register your models here.
from bioconverter.models import Converter, Conversing, BioImage, Locker, BioSeries

admin.site.register(Converter)
admin.site.register(Conversing)
admin.site.register(BioImage)
admin.site.register(Locker)
admin.site.register(BioSeries)