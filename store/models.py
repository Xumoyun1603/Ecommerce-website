from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name or self.user.username


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    @property
    def products(self):
        products = self.product_set.all()
        return products


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=False
    )
    name = models.CharField(max_length=200, null=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    price = models.PositiveBigIntegerField()
    description = models.TextField(blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    class Meta:
        unique_together = ['customer', 'date_orderd', 'complete', 'transaction_id']

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    phoneNumber = models.CharField(max_length=15, null=True)
    fullname = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    neighborhood = models.CharField(max_length=200, null=True)
    company_name = models.CharField(max_length=200, null=True)
    additional = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.region}, {self.city}, {self.neighborhood}."

