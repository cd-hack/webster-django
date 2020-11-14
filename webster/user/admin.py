from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CartProduct)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Rating)
