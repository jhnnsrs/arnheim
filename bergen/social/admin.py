from django.contrib import admin

# Register your models here.
from social.models import Comment

admin.site.register(Comment)