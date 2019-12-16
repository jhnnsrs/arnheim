from django.contrib import admin

# Register your models here.
from strainers.models import Strainer, Straining

admin.site.register(Strainer)
admin.site.register(Straining)