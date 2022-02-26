from datetime import date

from django.db import models

# Create your models here.

class User(models.Model):
    def __str__(self):
        return self.username
    username=models.CharField('User Name',max_length=100)
    email=models.EmailField('Email',max_length=100)
    contact=models.CharField('Contact No',max_length=12)
    password=models.CharField('Password',max_length=12)

    def exists(self):
        if User.objects.filter(email = self.email):
            return True
        return False

    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return False

class Product(models.Model):
    def __str__(self):
        return self.title
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/')
    price=models.FloatField()
    discount_price=models.FloatField()
    category=models.CharField(max_length=100)
    description=models.TextField()

    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in=ids)

class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    date = models.DateField(default=date.today)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=12)

    @staticmethod
    def get_orders_by_user(user_id):
        return Order.objects.filter(user = user_id)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    date = models.DateField(default=date.today)
