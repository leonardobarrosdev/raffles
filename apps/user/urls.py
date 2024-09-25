from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
	path("activate/<slug:uidb64>/<slug:token>/", views.activate, name="activate"),
    path("signin/", views.signin, name="signin"),
	path("signup/", views.SignupView.as_view(), name="signup"),
    path('signout', views.signout, name='signout'),
	path("<str:id>/", views.UpdateDetailsView.as_view(), name="update_details")
]
