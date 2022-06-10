from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'post_drf'
urlpatterns = [
    path('posts/', views.AllPosts.as_view() , name='AllPosts'),
    path('<int:post_id>/', views.PostDetail.as_view() , name='PostDetail'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)