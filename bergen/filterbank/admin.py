from django.contrib import admin

# Register your models here.
from filterbank.models import Filter, Parsing, Representation, NpArray, AImage

admin.site.register(Filter)
admin.site.register(Parsing)
admin.site.register(Representation)
admin.site.register(NpArray)
admin.site.register(AImage)