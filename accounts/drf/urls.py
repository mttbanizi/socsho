from django.urls import path

from rest_framework.authtoken import views

from .views import GetUsername, ObtainAuthToken,GetMyProfile

app_name = 'accounts_drf'

urlpatterns = [
    path('api-token-auth/', views.ObtainAuthToken.as_view()),
    path('getusername/<int:user_id>/', GetUsername.as_view() ),
    path('getprofile/', GetMyProfile.as_view() )
]