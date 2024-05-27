from django.forms import ModelForm
from .models import Raffle, AutomaticBuy, AwardedQuota, Promotion


class RaffleForm(ModelForm):
    class Meta:
        model = Raffle
        fields = '__all__'
        exclude = ['owner']


class AutomaticBuyForm(ModelForm):
    class Meta:
        model = AutomaticBuy
        fields = ['quantity', 'more_popular']


class PromotionForm(ModelForm):
    class Meta:
        model = Promotion
        fields = ['amount', 'price']


class AwardedQuotaForm(ModelForm):
    class Meta:
        model = AwardedQuota
        fields = ['number']
