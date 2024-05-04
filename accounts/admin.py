from django.contrib import admin
from .models import CustomUser, SocialAccount

admin.site.register(CustomUser)
admin.site.register(SocialAccount)