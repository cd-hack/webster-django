from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
# Create your models here.


class ClientProfile(models.Model):
    accNo = models.CharField(max_length=18)
    ifsc = models.CharField(max_length=12)
    plan = models.IntegerField()


class UserProfile(models.Model):
    website = models.ForeignKey(
        'client.Website', on_delete=models.CASCADE, null=True)


class ProfileManager(BaseUserManager):
    def create_user(self, email, name, phone, is_user, is_client, accNo=None, ifsc=None, plan=None, website=None, password=None):
        if not email:
            raise ValueError('email must have a value')
        if is_client == is_user:
            raise ValueError('You can either be a client or user')
        email = self.normalize_email(email)
        user = self.model()
        if is_user:
            wsite = None
            if website:
                Web = apps.get_model(app_label='client', model_name='Website')
                wsite = Web.objects.get(pk=website)
            up = UserProfile(website=wsite)
            up.save(using=self._db)
            user = self.model(email=email, name=name,
                              phone=phone, user_profile=up,is_user=is_user,is_client=is_client)
        if is_client:
            user = self.model(email=email, name=name, phone=phone)
            cp=ClientProfile(accNo=accNo, ifsc=ifsc, plan=plan)
            cp.save(using=self._db)
            user = self.model(email=email, name=name,
                              phone=phone, client_profile=cp,is_user=is_user,is_client=is_client)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        print(kwargs)
        user = self.create_user(email=kwargs['email'], name=kwargs['name'], phone=kwargs['phone'],is_user=kwargs['is_user'],is_client=kwargs['is_client'],
                                accNo=kwargs.get('accNo',12), ifsc=kwargs.get('ifsc',23), plan=kwargs.get('plan',1), password=kwargs['password'],website=kwargs.get('website',None))
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    is_client = models.BooleanField()
    is_user = models.BooleanField()
    is_staff = models.BooleanField(default=False)
    client_profile = models.OneToOneField(
        ClientProfile, on_delete=models.CASCADE, null=True)
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, null=True)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name', 'is_client', 'is_user']

    def __str__(self):
        return self.email


class Website(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField()
    templatetype = models.IntegerField()
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    ighandle = models.CharField(max_length=50)
    fburl = models.URLField()
    lnurl = models.URLField()
    image = models.ImageField()

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FashionProduct(models.Model):
    size = models.IntegerField()
    category = models.ManyToManyField(Category)


class FoodProduct(models.Model):
    veg = models.BooleanField()
    foodType = models.IntegerField()
    category = models.ManyToManyField(Category)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    description = models.TextField()
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    productType = models.IntegerField()
    fashion = models.OneToOneField(
        FashionProduct, on_delete=models.CASCADE, null=True)
    food = models.OneToOneField(
        FoodProduct, on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    available = models.BooleanField()

    def __str__(self):
        return self.name
