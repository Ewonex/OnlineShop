from django.contrib import admin

from .models import User, Item

admin.site.register(Item)
admin.site.register(User)
