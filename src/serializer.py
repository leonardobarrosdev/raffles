from rest_framework import serializers
from .models import Category, Raffle


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class RaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = '__all__'
