from django.contrib import admin

# Register your models here.
from biouploader.models import BioImage, Analyzing, BioSeries

admin.site.register(BioImage)
admin.site.register(Analyzing)
admin.site.register(BioSeries)