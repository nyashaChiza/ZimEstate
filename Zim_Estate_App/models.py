from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
# Create your models here.

fs = 'posts'


class Seller(models.Model):
    name = models.CharField(max_length=80)
    surname = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=80, unique=True, error_messages={'unique': 'This Email is already in use'})
    password = models.CharField(max_length=20)
    re_password = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @staticmethod
    def is_email_available(email):
        return Seller.objects.get(email=email)


class Property(models.Model):
    city = models.CharField(max_length=80)
    suburb = models.CharField(max_length=80, default='location(Suburb)')
    property_type = models.CharField(max_length=80)
    contract_type = models.CharField(max_length=80)
    description = models.CharField(max_length=600)
    size = models.IntegerField()
    price = models.IntegerField()
    views = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    interested = models.IntegerField(default=1)
    bedroom_num = models.IntegerField()
    bathroom_num = models.IntegerField()
    vacant = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=False)
    posted_on_facebook = models.BooleanField(default=False)
    date = models.DateField('date_posted', default=timezone.now())
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)

    def is_property_available(self):
        return self.vacant

    def is_property_validated(self):
        return self.is_valid

    def __str__(self):
        return self.suburb


class Buyer(models.Model):
    name = models.CharField(max_length=120)
    message = models.CharField(max_length=320, default=None)
    email = models.EmailField(max_length=80)
    phone_number = models.CharField(max_length=15)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    message = models.CharField(max_length=280)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)
    subject = models.CharField(max_length=80)

    def __str__(self):
        return self.name