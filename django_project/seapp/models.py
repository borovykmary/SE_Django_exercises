from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    available = models.BooleanField(default=True)

def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUSES = [
        ('new', 'New'),
        ('in_process', 'In Process'),
        ('sent', 'Sent'),
        ('completed', 'Completed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUSES)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def calculate_total_price(self):
        total_price = sum(product.price for product in self.products.all())
        return round(total_price, 2)

    def can_be_fulfilled(self):
        return all(product.available for product in self.products.all())