from django.contrib import admin

# Register your models here.
from revamper.models import Mask, Revamping, Revamper

admin.site.register(Mask)
admin.site.register(Revamping)
admin.site.register(Revamper)