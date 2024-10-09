import ipdb
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.product.models import Category, Product


class CategoryModelTest(TestCase):
    def test_create_category_success(self):
        category = Category.objects.create(name='Eletronic')
        self.assertIsInstance(category, Category)
        self.assertIs(str(category), 'Eletronic')

    def test_create_category_error(self):
        with self.assertRaises((TypeError, ValueError)):
            Category.objects.create(category='Auto')

    def test_category_obj_field(self):
        category = Category.objects.create(name='Moto Circle')
        field_length = category._meta.get_field('name').max_length
        self.assertEqual(field_length, 120)


class ProductModelTest(TestCase):
    fixtures = [
        'fixtures/category_fixture.json',
        'fixtures/user_fixture.json',
        'fixtures/product_fixture.json'
    ]
    def setUp(self):
        self.data = {
            "title": "Ebook",
            "number_quantity": 5,
            "price": "0.80",
            "min_quantity": 1,
            "digital": True,
            "description": "Ebook 7 codes of the intelligence",
            "create_at": "2024-10-01T20:23:00.000Z",
            "updated_at": "2024-10-01T20:23:00.000Z",
            "owner": get_user_model().objects.get(pk=8),
            "category": Category.objects.get(pk=4)
        }

    def test_create_product_success(self):
        product = Product.objects.create(**self.data)
        self.assertIsInstance(product, Product)
        self.assertTrue(product.digital)
        self.assertIsNotNone(product.number_quantity)

    def test_create_product_error(self):
        data = self.data.copy()
        del data['owner']
        with self.assertRaises(IntegrityError):
            Product.objects.create(**data)

    def test_product_obj_field(self):
        product = Product.objects.get(pk=1)
        field_label = product._meta.get_field('price').verbose_name
        max_length = product._meta.get_field('price').max_digits
        self.assertEqual(field_label, 'price')
        self.assertEqual(max_length, 10)