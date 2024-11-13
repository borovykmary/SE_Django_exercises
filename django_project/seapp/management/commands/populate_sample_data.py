from django.core.management.base import BaseCommand
from seapp.models import Product, Customer, Order


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='Sword of Tatsuka',
            price=598.87,
            available=True
        )
        product2 = Product.objects.create(
            name='Samehada weapon',
            price=785.99,
            available=True
        )
        product3 = Product.objects.create(
            name='kunai',
            price=144.29,
            available=False
        )
        customer1 = Customer.objects.create(
            name='Gaara',
            address='Hidden Sand 21/4'
        )
        customer2  = Customer.objects.create(
            name='Naruto',
            address='Hidden Leaf 5/1o'
        )
        customer3 = Customer.objects.create(
            name='Sasuke',
            address='Hidden Leaf 18/22'
        )
        order1 = Order.objects.create(
            customer=customer1,
            status='new'
        )
        order1.products.add(product1)
        self.stdout.write("Data created successfully.")

        order2 = Order.objects.create(
            customer=customer2,
            status='in_process'
        )
        order2.products.add(product2)
        self.stdout.write("Data created successfully.")

        order3 = Order.objects.create(
            customer=customer3,
            status='sent'
        )
        order3.products.add(product3)
        self.stdout.write("Data created successfully.")