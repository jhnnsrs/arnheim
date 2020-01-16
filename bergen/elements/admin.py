from django.contrib import admin

# Register your models here.
from bioconverter.models import Representation
from elements.models import Antibody, Sample, Experiment, Numpy, ExperimentalGroup, Zarr


class RepresentationInline(admin.TabularInline):
    model = Representation

class SampleAdmin(admin.ModelAdmin):
    inlines = [
        RepresentationInline,
    ]



admin.site.register(Antibody)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Experiment)
admin.site.register(Numpy)
admin.site.register(Zarr)
admin.site.register(ExperimentalGroup)