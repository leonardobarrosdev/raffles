from django.urls import path, re_path
from . import views

app_name = 'product'

urlpatterns = [
	path('list/', views.list, name='list'),
	path('create/', views.CreateView.as_view(), name='create'),
	path('<int:id>/', views.details, name='details'),
	path('<int:id>/delete/', views.delete, name='delete'),
	re_path(r'^(?P<id>[0-9]{1,4})/update(?:/(?P<image_id>[0-9]{1,5}))?/$', views.UpdateView.as_view(), name='update'),
]
