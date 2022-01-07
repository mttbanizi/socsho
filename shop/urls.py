from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'shop'
urlpatterns = [
	path('shop/', views.shop_home, name='home'),
	path('category/<slug:slug>/', views.shop_home, name='category_filter'),
	path('<slug:slug>/', views.product_detail, name='product_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)