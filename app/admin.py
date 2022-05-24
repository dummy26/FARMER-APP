from django.contrib import admin

from .models import (Bookmark, Delivery, Images, Machine, Order, OrderItem,
                     Residue, User)

admin.site.register(User)
admin.site.register(Machine)
admin.site.register(Images)
admin.site.register(Delivery)
admin.site.register(Bookmark)
admin.site.register(Residue)
admin.site.register(Order)
admin.site.register(OrderItem)
