from django.contrib import admin

# Register your models here.
from filterbank.models import Filter, Filtering

admin.site.register(Filter)
admin.site.register(Filtering)