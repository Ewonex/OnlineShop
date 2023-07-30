from django.contrib import admin

from .models import *

class RequestAdmin(admin.ModelAdmin):
    list_filter = ('status',)

admin.site.register(User)
admin.site.register(Brand)
admin.site.register(FavoriteItem)
admin.site.register(Review)
admin.site.register(Article)
admin.site.register(Vacansy)
admin.site.register(BucketItem)
admin.site.register(ReturningRequest, RequestAdmin)


