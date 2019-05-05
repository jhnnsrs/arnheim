from django.contrib import admin

# Register your models here.
from transformers.models import Transformation, Transforming, Transformer

admin.site.register(Transformation)
admin.site.register(Transforming)
admin.site.register(Transformer)