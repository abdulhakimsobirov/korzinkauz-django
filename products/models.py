from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    productCode = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=100, null=True)
    profilePic = models.ImageField(upload_to='ProfilePicture', null=True, default="defoult-user.png")
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
        
class Status(models.Model):
    name = models.CharField(max_length=100, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    orderCode = models.CharField(max_length=100, null=True)
    orderDate = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(Product, null=True)
    
    def __str__(self):
        return self.orderCode

