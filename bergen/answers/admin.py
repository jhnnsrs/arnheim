from django.contrib import admin

from answers.models import *

# Register your models here.
admin.site.register(Answer)
admin.site.register(Answering)
admin.site.register(Oracle)
admin.site.register(Question)