from rest_framework import serializers
from .models import UserProfile


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'email', 'cellfone', 'is_staff']


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'cpf',
            'email',
            'cellfone',
            'date_birth',
            'is_staff'
        ]
