from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.store.models import Order, ShippingAddress
from apps.product.models import Product


class StoreViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('store:home')

    def test_store_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_store_view_displays_products(self):
        # Create some products
        product1 = Product.objects.create(name='Product 1', price=10)
        product2 = Product.objects.create(name='Product 2', price=20)

        response = self.client.get(self.url)
        self.assertContains(response, product1.name)
        self.assertContains(response, product2.name)

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('cart')

    def test_cart_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')

    def test_add_to_cart(self):
        product = Product.objects.create(name='Product', price=10)
        data = {'product_id': product.id, 'quantity': 1}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().product, product)

class CheckoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('checkout')

    def test_checkout_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/checkout.html')

    def test_checkout_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/user/signin/?next=/checkout/')

    def test_checkout_view_post(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a shipping address
        address = ShippingAddress.objects.create(user=user, address='123 Main St', city='City', country='Country')

        # Add products to the cart
        product1 = Product.objects.create(name='Product 1', price=10)
        product2 = Product.objects.create(name='Product 2', price=20)
        order = Order.objects.create(user=user)
        order.products.add(product1, product2)

        data = {
            'shipping_address': address.id,
            'payment_method': 'credit_card',
            'card_number': '1234567890123456',
            'card_expiry': '12/23',
            'card_cvv': '123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(ShippingAddress.objects.count(), 0)
        self.assertTemplateUsed(response, 'store/order_success.html')