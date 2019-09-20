from django.contrib import admin

# Register your models here.
from elements.models import Antibody, Sample, Experiment

admin.site.register(Antibody)
admin.site.register(Sample)
admin.site.register(Experiment)