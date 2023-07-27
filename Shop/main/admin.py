from django.contrib import admin

from .models import *

admin.site.register(Item)
admin.site.register(User)
admin.site.register(Brand)
admin.site.register(FavoriteItem)
admin.site.register(Review)


