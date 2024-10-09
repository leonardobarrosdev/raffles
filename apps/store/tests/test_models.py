from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from apps.product.models import Product
from apps.store.models import *


PATH = 'fixtures/store'

class AddressModelTest(TestCase):
    fixtures = [
        'fixtures/user_fixture.json',
        f'{PATH}/order_fixture.json',
        f'{PATH}/address_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(id=5)
        self.order = Order.objects.get(id=9)

    def test_create_address_success(self):
        address = ShippingAddress.objects.create(
            customer=self.user,
            order=self.order,
            address='Pine Road',
            number=28,
            city='Chicago',
            state='IL',
            zipcode=60601
        )
        self.assertEqual(ShippingAddress.objects.count(), 11)
        self.assertEqual(str(address), 'Chicago - IL')
        self.assertEqual(address.customer.id, self.user.id)

    def test_create_address_error(self):
        with self.assertRaises(ValueError):
            ShippingAddress.objects.create(
                customer=self.user,
                order=self.order,
                address='Pine Road',
                number=28,
                city='Chicago',
                state='IL',
                zipcode=''
            )

    def test_address_obj_field(self):
        address = ShippingAddress.objects.get(id=4)
        field_label = address._meta.get_field('state').verbose_name
        max_length = address._meta.get_field('state').max_length
        self.assertIsInstance(address, ShippingAddress)
        self.assertEqual(field_label, 'state')
        self.assertEqual(max_length, 2)


class AutomaticBuyModelTest(TestCase):
    fixtures = [
        'fixtures/user_fixture.json',
        'fixtures/category_fixture.json',
        'fixtures/product_fixture.json',
        f'{PATH}/automatic_buy_fixture.json'
    ]

    def setUp(self):
        self.product = Product.objects.get(id=3)

    def test_create_automatic_success(self):
        automatic = AutomaticBuy.objects.create(
            product=self.product,
            quantity=2,
            more_popular=True
        )
        self.assertEqual(AutomaticBuy.objects.count(), 11)
        self.assertEqual(automatic.product, self.product)
        self.assertTrue(automatic.more_popular)

    def test_create_automatic_error(self):
        with self.assertRaises((ValueError, IntegrityError)):
            AutomaticBuy.objects.create(
                quantity=2,
                more_popular=None
            )

    def test_automatic_obj_field(self):
        automatic = AutomaticBuy.objects.get(id=4)
        field_label = automatic._meta.get_field('quantity').verbose_name
        default = automatic._meta.get_field('quantity').default
        self.assertIsInstance(automatic, AutomaticBuy)
        self.assertEqual(field_label, 'quantity')
        self.assertEqual(default, 0)


class OrderModelTest(TestCase):
    fixtures = ['fixtures/user_fixture.json', f'{PATH}/order_fixture.json']

    def setUp(self):
        self.user = get_user_model().objects.get(id=6)

    def test_create_order_success(self):
        order = Order.objects.create(customer=self.user, status='P')
        self.assertEqual(Order.objects.count(), 11)
        self.assertEqual(order.customer, self.user)
        self.assertEqual(str(order), 'P')

    def test_create_order_error(self):
        with self.assertRaises(ValueError):
            Order.objects.create(customer='')

    def test_order_obj_field(self):
        order = Order.objects.get(id=8)
        field_label = order._meta.get_field('status').verbose_name
        is_relation = order._meta.get_field('customer').is_relation
        self.assertIsInstance(order, Order)
        self.assertEqual(field_label, 'status')
        self.assertTrue(is_relation)


class PromotionModelTest(TestCase):
    fixtures = [
        'fixtures/user_fixture.json',
        'fixtures/category_fixture.json',
        'fixtures/product_fixture.json',
        f'{PATH}/promotion_fixture.json'
    ]

    def setUp(self):
        self.product = Product.objects.get(id=7)

    def test_create_promotion_success(self):
        promotion = Promotion.objects.create(product=self.product, amount=4, price=5.70)
        self.assertEqual(Promotion.objects.count(), 11)
        self.assertEqual(promotion.product, self.product)
        self.assertEqual(promotion.price, 5.70)

    def test_create_promotion_error(self):
        promotion = Promotion.objects.create(price=2.35)
        self.assertIsNone(promotion.product)

    def test_promotion_obj_field(self):
        promotion = Promotion.objects.get(id=10)
        is_relation = promotion._meta.get_field('product').is_relation
        field_label = promotion._meta.get_field('amount').verbose_name
        default = promotion._meta.get_field('price').default
        self.assertTrue(is_relation)
        self.assertEqual(field_label, 'amount')
        self.assertEqual(default, 0.0)


class AwardedQuotaModelTest(TestCase):
    fixtures = [
        'fixtures/user_fixture.json',
        'fixtures/category_fixture.json',
        'fixtures/product_fixture.json',
        f'{PATH}/quota_fixture.json'
    ]

    def setUp(self):
        self.product = Product.objects.get(id=2)

    def test_create_quota_success(self):
        quota = AwardedQuota.objects.create(product=self.product, number=3)
        self.assertEqual(AwardedQuota.objects.count(), 11)
        self.assertEqual(quota.product, self.product)
        self.assertEqual(quota.number, 3)

    def test_create_quota_error(self):
        with self.assertRaises(AttributeError):
            AwardedQuota.object.create()

    def test_quota_obj_field(self):
        quota = AwardedQuota.objects.get(id=3)
        auto_created = quota._meta.get_field('id').auto_created
        is_relation = quota._meta.get_field('number').is_relation
        self.assertIsInstance(quota, AwardedQuota)
        self.assertTrue(auto_created)
        self.assertFalse(is_relation)