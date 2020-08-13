from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_image_url(self):
        try:
            return self.image.url
        except:
            return ''


class Order(models.Model):
    customer = models.ForeignKey("store.Customer", on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        return sum([item.get_total for item in self.orderitem_set.all()])

    @property
    def get_cart_items(self):
        return sum([item.quantity for item in self.orderitem_set.all()])

    @property
    def is_shipping(self):
        is_shipping = False

        for item in self.orderitem_set.all():
            if not item.product.digital:
                is_shipping = True

        return is_shipping


class OrderItem(models.Model):
    product = models.ForeignKey("store.Product", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey("store.Order", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey("store.Customer", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey("store.Order", on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
