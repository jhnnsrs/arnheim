from django.contrib import admin

# Register your models here.
from metamorphers.models import Metamorpher, Metamorphing, Exhibit, Display

admin.site.register(Metamorpher)
admin.site.register(Exhibit)
admin.site.register(Display)
admin.site.register(Metamorphing)