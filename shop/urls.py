from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'shop'
urlpatterns = [
	path('shop/', views.shop_home, name='home'),
	path('shop/select_category/', views.select_category, name='select_category'),
	path('shop/<slug:category_slug>/', views.shop_home, name='category_filter'),
	path('add_product/<int:user_id>/', views.AddProduct.as_view(), name='add_product'),
	path('manage_products/<int:user_id>/', views.manage_products, name='manage_products'),
	path('product_reply/<int:product_id>/<int:comment_id>/', views.product_reply, name='product_reply'),
	path('product_like/<int:product_id>/', views.product_like, name='product_like'),
	path('product_remove/<int:pk>/', views.ProductDeleteView.as_view(), name='product_remove'),
	path('product_update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
	


	path('product_dislike/<int:product_id>/', views.product_dislike, name='product_dislike'),
	path('<slug:slug>/', views.product_detail, name='product_detail'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)