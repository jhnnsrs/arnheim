from django.contrib import admin

# Register your models here.
from elements.models import Antibody, Sample, Experiment, ExperimentalGroup, Representation, Transformation


class RepresentationInline(admin.TabularInline):
    model = Representation

class SampleAdmin(admin.ModelAdmin):
    inlines = [
        RepresentationInline,
    ]


admin.site.register(Transformation)
admin.site.register(Antibody)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Experiment)
admin.site.register(Representation)
admin.site.register(ExperimentalGroup)