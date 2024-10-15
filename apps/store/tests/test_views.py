import json, ipdb

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, tag
from django.urls import reverse
from django.contrib.auth.models import User
from apps.store.models import Order, ShippingAddress
from apps.product.models import Product


PATH = 'fixtures/store'

class StoreViewTest(TestCase):
    fixtures = [
        'fixtures/user_fixture.json',
        'fixtures/category_fixture.json',
        'fixtures/product_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('store:home')

    def test_store_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_store_view_displays_products(self):
        product1 = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        response = self.client.get(self.url)
        self.assertEqual(response.context['products'].get(id=1), product1)
        self.assertEqual(response.context['products'].get(id=2), product2)


class CartViewTest(TestCase):
    fixtures = [
        'fixtures/user_fixture.json',
        'fixtures/category_fixture.json',
        'fixtures/product_fixture.json',
        f'{PATH}/order_fixture.json'
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('store:cart')
        self.credentials = {'email': 'alice@company.com', 'password': '123456'}

    def test_cart_success(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class AddSubItemViewTest(TestCase):
    fixtures = [
        'fixtures/user_fixture.json',
        'fixtures/category_fixture.json',
        'fixtures/product_fixture.json',
        f'{PATH}/order_fixture.json'
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(email='alice@company.com', password='123456')
        self.url = reverse('store:add-subitems', kwargs={'product_id': 8})
        self.user = get_user_model().objects.get(id=5)
        self.product = Product.objects.get(id=8)
        self.mocked_data = {
            'order_id': Order.objects.filter(customer=self.user, status='P').first().id,
            'item_title': self.product.title,
            'subitems': [66, 90]
        }

    def test_add_subitem_to_cart_success(self):
        self.client.cookies['numbers'] = json.dumps([66, 90])
        response = self.client.post(self.url)
        self.assertJSONEqual(response.content, self.mocked_data)
        self.assertTemplateUsed(reverse('raffle:raffle'))

    def test_add_subitem_to_cart_error(self):
        self.client.cookies['numbers'] = json.dumps([66, 90])
        response = self.client.post(self.url)
        self.assertJSONEqual(response.content, self.mocked_data)
        self.assertTemplateUsed(reverse('raffle:raffle'))

    def test_add_subitem_to_cart_product_not_found(self):
        self.client.cookies['numbers'] = json.dumps([66, 90])
        response = self.client.post(reverse('store:add-subitems', kwargs={'product_id': 9999}))
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error': 'Product not found'})

    def test_add_subitem_to_cart_missing_cookie(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Numbers cookie missing'})

    def test_add_subitem_to_cart_unauthorized(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to login page
        self.assertRedirects(response, reverse('user:signin') + '?next=' + self.url)


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('store:checkout')

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