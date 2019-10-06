from django.contrib import admin

# Register your models here.
from elements.models import Antibody, Sample, Experiment, Numpy, ExperimentalGroup

admin.site.register(Antibody)
admin.site.register(Sample)
admin.site.register(Experiment)
admin.site.register(Numpy)
admin.site.register(ExperimentalGroup)