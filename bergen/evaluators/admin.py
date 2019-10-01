from django.contrib import admin

from evaluators.models import *
# Register your models here.
admin.site.register(Evaluating)
admin.site.register(Evaluator)
admin.site.register(Data)
admin.site.register(VolumeData)
admin.site.register(ClusterData)