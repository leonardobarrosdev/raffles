from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
	path('list/', views.list, name='list'),
	path('create/', views.CreateView.as_view(), name='create'),
	path('<int:id>/', views.details, name='details'),
	path('<int:id>/update/', views.UpdateView.as_view(), name='update'),
	path('<int:id>/delete/', views.delete, name='delete'),
	path('image/', views.ImageView.as_view(), name='image'),
]
