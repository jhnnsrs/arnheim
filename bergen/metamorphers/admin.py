from django.contrib import admin

# Register your models here.
from metamorphers.models import Metamorpher, Metamorphing, Exhibit, Display

# NodeModels
admin.site.register(Metamorpher)
admin.site.register(Metamorphing)

# Data Models
admin.site.register(Exhibit)
admin.site.register(Display)