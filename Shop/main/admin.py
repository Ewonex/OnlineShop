from django.contrib import admin

from .models import *

class RequestAdmin(admin.ModelAdmin):
    list_filter = ('status',)

class OrderItemAdmin(admin.ModelAdmin):
    list_filter = ('order__id',)


admin.site.register(User)
admin.site.register(Item)
admin.site.register(Brand)
admin.site.register(FavoriteItem)
admin.site.register(Review)
admin.site.register(Article)
admin.site.register(Vacansy)
admin.site.register(BucketItem)
admin.site.register(Order, RequestAdmin)
admin.site.register(ItemOfTheOrder, OrderItemAdmin)
admin.site.register(ReturningRequest, RequestAdmin)


