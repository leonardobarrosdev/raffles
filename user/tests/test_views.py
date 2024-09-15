from django.test import TestCase, Client, tag
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from user.authentify.token import AppTokenGenerator
from ..forms import SignupForm
from ..views import send_email_welcome


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.mocked_email = 'test@example.com'
        self.data = {
            'email': self.mocked_email,
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'cpf': '12345678901',
            'phone': '12345678901',
            'date_birth': '2000-01-01'
        }
        self.user = self.User.objects.create_user(**self.data)

    def tearDown(self) -> None:
        return super().tearDown()
    
    @tag('signup')
    def test_signup_view_get(self):
        response = self.client.get(reverse('user:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertIsInstance(response.context['form'], SignupForm)

    @tag('signup')
    def test_signup_view_post(self):
        response = self.client.post(reverse('user:signup'), {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'cpf': '12345679801',
            'phone': '12345608901',
            'date_birth':'2000-01-01',
            'password': 'newpassword',
            'password2': 'newpassword',
            'terms': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.User.objects.count(), 2)
        self.assertTrue(self.User.objects.filter(email='newuser@example.com').exists())

    @tag('signup')
    def test_signup_view_post_failure(self):
        response = self.client.post(reverse('user:signup'), {
            'first_name': 'Exist',
            'last_name': 'User',
            'email': '',
            'cpf': '12345679801',
            'phone': '12325678901',
            'date_birth': '2000-01-01',
            'password': 'newpassword',
            'password2': 'newpassword',
            'terms': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.failIf(response.context['form'].is_valid())

    @tag('send_email')
    def test_send_email_welcome_view(self):
        user = self.User.objects.create_user(
            first_name='New',
            email='newuser@example.com',
            password='newpassword'
        )
        send_email_welcome(user.first_name, user.email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['newuser@example.com'])
        self.assertEqual(mail.outbox[0].subject, 'Welcome to your Website from Raffles!')

    @tag('active')
    def test_active_view(self):
        token = AppTokenGenerator().make_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        activate_url = reverse('user:activate', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.get(activate_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:signin'))
        self.assertTrue(self.User.objects.get(id=self.user.id).is_active)

    @tag('signin')
    def test_signin_view(self):
        request = self.client.get(reverse('user:signin')).wsgi_request
        current_site = get_current_site(request)
        protocol = 'https' if request.is_secure() else 'http'
        activate_url = reverse('user:activate', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(self.user.id)),
            'token': AppTokenGenerator().make_token(self.user)
        })
        self.client.get('%s://%s%s' % (protocol, current_site.domain, activate_url))
        response = self.client.post(reverse('user:signin'), data={
            'email': self.mocked_email,
            'password': 'testpassword'
        })
        self.assertIsNotNone(current_site)
        self.assertTrue(self.client.session['_auth_user_id'])
        self.assertRedirects(response, reverse('store:home'))
    
    @tag('signin')
    def test_signin_view_failure(self):
        response = self.client.post(reverse('user:signin'), data={
            'email': 'error@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:signin'))

    def test_signout_view(self):
        response = self.client.get(reverse('user:signout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('store:home'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_update_details_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        user = self.User.objects.get(email='test@example.com')
        update_details_url = reverse('user:update_details', kwargs={'id': user.id})
        response = self.client.post(update_details_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '31996692393',
            'email': user.email,
            'cpf': user.cpf,
            'date_birth': user.date_birth,
            'password': 'testpassword'
        })
        updated_user = self.User.objects.get(id=user.id)
        self.assertEqual(updated_user.first_name, 'John')
        self.assertEqual(updated_user.last_name, 'Doe')
        self.assertEqual(updated_user.phone, '31996692393')
        self.assertEqual(response.status_code, 302)
