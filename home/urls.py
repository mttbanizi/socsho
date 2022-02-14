from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
	path('', views.all_home, name='all_home'),
	path('category_filter/<slug:slug>/', views.all_home, name='category_filter'),

	
]