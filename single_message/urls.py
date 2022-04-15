# chat/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name= 'single_message'
urlpatterns = [
    #path('', views.index, name='index'),
    #path('<str:room_name>/', views.room, name='room'),
    path('dual_room_id/<str:user_id>/', views.dual_room_id, name='dual_room_id'),
    path('dual_room/', views.dual_room, name='dual_room'),

    path('dual_room_email/<str:email>/', views.dual_room_email, name='dual_room_email'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)