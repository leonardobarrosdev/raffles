from django.test import TestCase, Client, tag
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from ..utils import AppTokenGenerator
from ..models import UserProfile
from ..forms import SignupForm
from ..views import SignupView
from ..views import send_email_welcome
import ipdb

class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('user:signup')
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            cpf='12345678901',
            phone='12345678901',
            date_birth='2000-01-01'
        )

    @tag('signup')
    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertIsInstance(response.context['form'], SignupForm)

    @tag('signup')
    def test_signup_view_post_success(self):
        response = self.client.post(self.signup_url, {
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
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertTrue(UserProfile.objects.filter(email='newuser@example.com').exists())

    @tag('signup')
    def test_signup_view_post_failure(self):
        response = self.client.post(self.signup_url, {
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
        self.assertTemplateUsed(response, 'user/email_confirmation.html')
        # self.assertFormError(response, 'form', 'email', 'Email already registered.')

    def test_send_email_welcome_view(self):
        user = UserProfile.objects.create_user(
            first_name='New',
            email='newuser@example.com',
            password='newpassword'
        )
        send_email_welcome(user.first_name, user.email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to your Website from Raffles!')

    @tag('activate')
    def test_activate_view(self):
        token = AppTokenGenerator().make_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        activate_url = reverse('user:activate', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.get(activate_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:signin'))
        self.assertTrue(UserProfile.objects.get(pk=self.user.pk).is_active)

    @tag('signin')
    def test_signin_view(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.post(reverse('user:signin'), {
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('store:home'))
    
    @tag('signin')
    def test_signin_view_failure(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.post(reverse('user:signin'), {
            'email': 'error@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signin.html')
        # self.assertFormError(response, 'form', None, 'Email or password is incorrect.')

    def test_signout_view(self):
        response = self.client.get(reverse('user:signout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('store:home'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_update_details_view(self):
        self.client.login(email='test@example.com', password='testpassword')
        user = UserProfile.objects.get(email='test@example.com')
        update_details_url = reverse('user:update_details', kwargs={'id': user.id})
        response = self.client.post(update_details_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '31996692393',
            'email': user.email,
            'cpf': user.cpf,
            'date_birth': user.date_birth,
            'password': 'testpassword',
            'password2': 'testpassword',
            'terms': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:update_details', kwargs={'id': user.id}))
        updated_user = UserProfile.objects.get(id=user.id)
        self.assertEqual(updated_user.first_name, 'John')
        self.assertEqual(updated_user.last_name, 'Doe')
        self.assertEqual(updated_user.phone, '31996692393')