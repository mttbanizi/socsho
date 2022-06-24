from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'post_drf'
urlpatterns = [
    path('posts/', views.AllPosts.as_view() , name='AllPosts'),
    path('<int:post_id>/', views.PostDetail.as_view() , name='PostDetail'),
    path('reply/', views.AddReply.as_view() , name='AddReply'),
    path('comment/', views.AddComment.as_view() , name='AddComment'),
    path('like/<int:post_id>/', views.PostLike.as_view() , name='PostLike'),
    path('<int:post_id>/<int:user_id>/', views.PostLike.as_view() , name='PostLike'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)