from django.urls import path
from . import views


app_name = 'post_drf'
urlpatterns = [
    path('posts/', views.AllPosts.as_view() , name='AllPosts'),
    
]