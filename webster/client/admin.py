from django.contrib import admin
from client import models
# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Product)
admin.site.register(models.Website)
admin.site.register(models.Category)
admin.site.register(models.FashionProduct)
admin.site.register(models.FoodProduct)
admin.site.register(models.ClientProfile)
admin.site.register(models.UserProfile)


