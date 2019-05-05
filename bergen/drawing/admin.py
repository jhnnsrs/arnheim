from django.contrib import admin

# Register your models here.
from drawing.models import ROI, Sample, BioMeta

admin.site.register(ROI)
admin.site.register(Sample)
admin.site.register(BioMeta)
