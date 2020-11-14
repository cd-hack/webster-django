from django.db import models
# from client.models import Website, Product


class Order(models.Model):
    orderDate = models.DateField(auto_now=True)
    user = models.ForeignKey('client.Profile', on_delete=models.CASCADE)
    website = models.ForeignKey('client.Website', on_delete=models.CASCADE)


class CartProduct(models.Model):
    user = models.ForeignKey(
        'client.Profile', null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product = models.ForeignKey(
        'client.Product', null=True, on_delete=models.CASCADE)
    #total = models.DecimalField(decimal_places=2, max_digits=8)
    @property
    def total(self):
       _total = self.quantity*self.product.price
       return total


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(
        'client.Product', null=True, on_delete=models.CASCADE)
    #total = models.DecimalField(decimal_places=2, max_digits=8)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    @property
    def total(self):
       _total = self.quantity*self.product.price
       return total


class Rating(models.Model):
    userprofile = models.ForeignKey('client.Profile', on_delete=models.CASCADE)
    product = models.ForeignKey('client.Product', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(null=True, blank=True)


class Wishlist(models.Model):
    userprofile = models.ForeignKey('client.Profile', on_delete=models.CASCADE)
    product = models.ForeignKey('client.Product', on_delete=models.CASCADE)
