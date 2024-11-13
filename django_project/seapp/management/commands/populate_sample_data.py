from django.core.management.base import BaseCommand
from seapp.models import Product, Customer, Order


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='...',
            price=19.99,
            available=True
        )
        customer1 = Customer.objects.create(
            name='...',
            address='...'
        )
        order1 = Order.objects.create(
            customer=customer1,
            status='...'
        )
        order1.products.add(product1)
        self.stdout.write("Data created successfully.")