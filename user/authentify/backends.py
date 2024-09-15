from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmailAuthenticate(BaseBackend):
    User = get_user_model()

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            user = self.User.objects.get(Q(username=username) | Q(email=email))
        except self.User.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return self.User.objects.filter(email=email).order_by('id').first()
        if user.check_password(password):
            return user
        return None

    def get_user(self,user_id):
        try:
            return self.User.objects.get(pk=user_id)
        except self.User.DoesNotExist:
            return None