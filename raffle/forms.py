from django.forms import ModelForm
from .models import Raffle


class RaffleForm(ModelForm):
    class Meta:
        model = Raffle
        fields = '__all__'
        exclude = ['owner']
