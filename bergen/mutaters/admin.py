from django.contrib import admin

# Register your models here.
from mutaters.models import *

admin.site.register(Mutater)
admin.site.register(Mutating)
admin.site.register(Reflection)