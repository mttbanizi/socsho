# chat/urls.py
from django.urls import path

from . import views

app_name= 'single_message'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('dual_room/<str:user_id>/', views.dual_room, name='dual_room'),
]