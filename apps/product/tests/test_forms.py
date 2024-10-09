import ipdb
from django.http import HttpRequest
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.product.models import Category, Product
from apps.product.forms import ProductForm


class ProductFormTest(TestCase):
    fixtures = [
        'fixtures/category_fixture.json',
        'fixtures/user_fixture.json',
        'fixtures/product_fixture.json'
    ]

    def setUp(self):
        self.request = HttpRequest()
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

    def test_product_form_success(self):
        form = ProductForm(data=self.data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Product.objects.count(), 11)

    def test_product_form_error(self):
        data = self.data.copy()
        data['title'] = ''
        form = ProductForm(data=data)
        self.assertEqual(form.errors['title'], ['Este campo é obrigatório.'])
        with self.assertRaises(ValueError):
            form.save()

    def test_product_request_success(self):
        self.request.POST = self.data
        form = ProductForm(self.request.POST)
        self.assertTrue(form.fields['digital'])

    def test_product_request_error(self):
        self.request.POST = self.data
        form = ProductForm(self.request.POST)
        self.assertFalse(form.fields['digital'].disabled)