from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'accounts'
urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('register/', views.user_register, name='register'),
	path('dashboard/<int:user_id>/', views.user_dashboard, name='dashboard'),
	path('profile_update/<int:pk>/', views.ProfileUpdate.as_view(), name='profile_update'),
	path('follow/', views.follow, name='follow'),
	path('unfollow/', views.unfollow, name='unfollow'),
	path('show_photo/<int:pk>/', views.show_photo, name='show_photo'),
	path('update_photo/<int:user_id>/<int:image_id>', views.update_photo, name='update_photo'),
	path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
	path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
	path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('requests/', views.follow_requests.as_view(), name='requests'),
	path('accept_request/', views.accept_request, name='accept_request'),
	path('follower_list/', views.follower_list.as_view(), name='follower_list'),
	path('reject_follow/', views.reject_follow, name='reject_follow'),

	path('following_list/', views.following_list.as_view(), name='following_list'),
	path('cancel_following/', views.cancel_following, name='cancel_following'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)