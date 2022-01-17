from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'shop'
urlpatterns = [
	path('shop/', views.shop_home, name='home'),
	path('category/<slug:slug>/', views.shop_home, name='category_filter'),
	path('add_product/<int:user_id>/', views.AddProduct.as_view(), name='add_product'),
	path('<slug:slug>/', views.product_detail, name='product_detail'),
	path('add_reply/<int:product_id>/<int:comment_id>/', views.add_reply, name='add_reply'),
	path('product_like/<int:product_id>/', views.product_like, name='product_like'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)