from django.db import models
from client.models import Website, Product


class UserProfile(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

class Order(models.Model):
    orderDate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

class CartProduct(models.Model):
    user = models.ForeignKey(UserProfile, null=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=8)

class OrderProduct(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=8)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Rating(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(null=True,blank=True)


class Wishlist(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

