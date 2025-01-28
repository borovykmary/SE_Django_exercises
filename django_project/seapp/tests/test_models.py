from django.test import TestCase
from seapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product',
        price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product',
                                          price=-1.99, available=True)
            temp_product.full_clean()

    # Negative Test Case: Product creation with missing name
    def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(price=1.99, available=True)
            temp_product.full_clean()

    # Negative Test Case: Product creation with blank name
    def test_create_product_with_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='', price=1.99, available=True)
            temp_product.full_clean()

    # Negative Test Case: Product creation with missing price
    def test_create_product_with_missing_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='No Price Product', available=True)
            temp_product.full_clean()


    # Negative Test Case: Product creation with invalid price format
    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name='Invalid Price Format', price=10.123, available=True
            )
            temp_product.full_clean()

    # Positive Test Case: Product creation with minimum valid price
    def test_create_product_with_minimum_valid_price(self):
        temp_product = Product.objects.create(name='Min Price Product', price=0.01, available=True)
        self.assertEqual(temp_product.price, 0.01)

    # Negative Test Case: Product creation with price below minimum
    def test_create_product_with_price_below_minimum(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name='Below Min Price', price=0.00, available=True
            )
            temp_product.full_clean()

    # Negative Test Case: Product creation with price exceeding maximum
    def test_create_product_with_price_above_maximum(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name='Exceed Max Price', price=1000000.01, available=True
            )
            temp_product.full_clean()

    # Positive Test Case: Product creation with minimum name length
    def test_create_product_with_minimum_name_length(self):
        temp_product = Product.objects.create(name='A', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'A')

    # Negative Test Case: Product creation with name exceeding max length
    def test_create_product_with_name_exceeding_max_length(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(
                name='A' * 256,
                price=1.99, available=True
            )
            temp_product.full_clean()

class CustomerModelTest(TestCase):
    # Positive Test Case: Customer creation with valid data
    def test_create_customer_with_valid_data(self):
        customer = Customer.objects.create(
            name='Temari', address='Hidden Sand 21/4'
        )
        self.assertEqual(customer.name, 'Temari')
        self.assertEqual(customer.address, 'Hidden Sand 21/4')

    # Negative Test Case: Customer creation with missing name
    def test_create_customer_with_missing_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer.objects.create(address='Hidden Sand 21/4')
            customer.full_clean()

    # Negative Test Case: Customer creation with blank name
    def test_create_customer_with_blank_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer.objects.create(name='', address='Hidden Sand 21/4')
            customer.full_clean()

    # Negative Test Case: Customer creation with missing address
    def test_create_customer_with_missing_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer.objects.create(name='Temari')
            customer.full_clean()

    # Negative Test Case: Customer creation with blank address
    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer.objects.create(name='Temari', address='')
            customer.full_clean()

    # Positive Test Case: Customer creation with minimum name length
    def test_create_customer_with_minimum_name_length(self):
        customer = Customer.objects.create(name='A', address='Hidden Sand 21/4')
        self.assertEqual(customer.name, 'A')

    # Negative Test Case: Customer creation with maximum name length
    def test_create_customer_with_name_max_length(self):
        customer = Customer.objects.create(name='A'* 100, address='Hidden Sand 21/4')
        self.assertEqual(customer.name, 'A'* 100)



class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(name='Temari', address='Hidden Sand 21/4')
        self.product1 = Product.objects.create(name='Product 1', price=10.00, available=True)
        self.product2 = Product.objects.create(name='Product 2', price=20.00, available=False)

    # Positive Test Case: Order creation with valid data
    def test_create_order_with_valid_data(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, 'New')
        self.assertIn(self.product1, order.products.all())

    # Negative Test Case: Order creation without a customer
    def test_create_order_without_customer(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=None, status='New')
            order.full_clean()

    # Negative Test Case: Order creation without a status
    def test_create_order_without_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status=None)
            order.full_clean()

    # Negative Test Case: Order creation with an invalid status
    def test_create_order_with_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status='InvalidStatus')
            order.full_clean()

    # Positive Test Case: Total price calculation with valid products
    def test_total_price_calculation_with_valid_products(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1, self.product2)
        total_price = sum(product.price for product in order.products.all())
        self.assertEqual(total_price, 30.00)

    # Positive Test Case: Total price calculation with no products
    def test_total_price_calculation_with_no_products(self):
        order = Order.objects.create(customer=self.customer, status='New')
        total_price = sum(product.price for product in order.products.all())
        self.assertEqual(total_price, 0.00)

    # Test Case: Order fulfillment with product availability
    def test_order_fulfillment_with_product_availability(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1, self.product2)

        can_fulfill = all(product.available for product in order.products.all())
        self.assertFalse(can_fulfill)

        order.products.remove(self.product2)
        can_fulfill = all(product.available for product in order.products.all())
        self.assertTrue(can_fulfill)
