from django.contrib.auth import get_user_model
from django.forms import ModelForm


class UserProfileForm(ModelForm):
	class Meta:
		model = get_user_model()
		fields = '__all__'
		exclude = ['is_staff']
