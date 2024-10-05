from django.urls import path, re_path
from . import views

app_name = 'user'

urlpatterns = [
    path("signin/", views.signin, name="signin"),
	path("signup/", views.SignupView.as_view(), name="signup"),
    path("signout/", views.signout, name='signout'),
	path("<int:pk>/", views.UpdateDetailsView.as_view(), name="update_details"),
	path("activate/<slug:uidb64>/<slug:token>/", views.activate, name="activate"),
	# re_path(r"^(?P<pk>[0-9]+)/$", views.UpdateDetailsView.as_view(), name="update_details"),
]
