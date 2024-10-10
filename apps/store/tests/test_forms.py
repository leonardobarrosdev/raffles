from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.store.forms import  ShippingAddressForm
from apps.store.models import Order


PATH = 'fixtures/store'

class ShippingAddressFormTest(TestCase):
    fixtures = [
        'fixtures/user_fixture.json',
        f'{PATH}/order_fixture.json',
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(id=4)
        self.order = Order.objects.get(id=5)
        self.data = {
            'customer': self.user,
            'order': self.order,
            'address': 'Cedar Boulevard',
            'number': 54,
            'neighborhood': 'Cedar Boulevard',
            'city': 'Houston',
            'state': 'TX',
            'zipcode': 77010
        }

    def test_valid_form(self):
        form = ShippingAddressForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = self.data.copy()
        del data['address']
        form = ShippingAddressForm(data=data)
        self.assertFalse(form.is_valid())
