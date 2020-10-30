from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
# Create your models here.


class ClientProfileManager(BaseUserManager):
    def create_user(self, email, name, phone, accNo, ifsc, plan, password=None):
        if not email:
            raise ValueError('email must have a value')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone,
                          accNo=accNo, ifsc=ifsc, plan=plan)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, *args, **kwargs):
        print(kwargs)
        user = self.model(email=kwargs['email'], name=kwargs['name'], phone=kwargs['phone'],
                          accNo=kwargs['accNo'], ifsc=kwargs['ifsc'], plan=kwargs['plan'])
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class ClientProfile(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    accNo = models.CharField(max_length=15)
    ifsc = models.CharField(max_length=12)
    plan = models.IntegerField()

    objects = ClientProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name', 'ifsc', 'accNo', 'plan']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=255)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class Website(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField()
    templatetype = models.IntegerField()
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    ighandle = models.CharField(max_length=50)


class FashionProduct(models.Model):
    size = models.IntegerField()
    category = models.ManyToManyField(Category)


class FoodProduct(models.Model):
    veg = models.BooleanField()
    ftype = models.IntegerField()
    category = models.ManyToManyField(Category)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    description = models.TextField()
    orderproduct = models.ForeignKey(
        OrderProduct, on_delete=models.CASCADE, null=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    ptype = models.IntegerField()
    fashion = models.OneToOneField(
        FashionProduct, on_delete=models.CASCADE, null=True)
    food = models.OneToOneField(
        FoodProduct, on_delete=models.CASCADE, null=True)


class Image(models.Model):
    website = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.ImageField()


class UserProfile(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=30)



class CartProduct(models.Model):
    cart=models.ForeignKey(UserProfile,null=True)
    quantity = models.IntegerField()
    total = models.DecimalField(decimal_places=2, max_digits=8)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Order(models.Model):
    orderDate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    total = models.DecimalField(decimal_places=2, max_digits=8)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Rating(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()


class Wishlist(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
