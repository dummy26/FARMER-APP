from django.contrib import admin

from .models import (Bookmark, CartItem, Delivery, Machine, Order, RentOrder,
                     Residue, ResidueOrder, User)

admin.site.register(User)
admin.site.register(Machine)
admin.site.register(Delivery)
admin.site.register(Bookmark)
admin.site.register(Residue)
admin.site.register(Order)
admin.site.register(RentOrder)
admin.site.register(CartItem)
admin.site.register(ResidueOrder)
