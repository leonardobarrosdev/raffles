from rest_framework import serializers
from .models import Raffle


class RaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = '__all__'

# class RafflePurchaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Raffle
#         fields = ['id', 'user', 'quantity']

# class RafflePaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Raffle
#         fields = ['id', 'payment_status']
