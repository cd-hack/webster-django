from django.contrib import admin
from client import models
# Register your models here.
admin.site.register(models.ClientProfile)
admin.site.register(models.Image)
admin.site.register(models.Order)
admin.site.register(models.OrderProduct)
admin.site.register(models.Product)
admin.site.register(models.Rating)
admin.site.register(models.Website)
admin.site.register(models.UserProfile)