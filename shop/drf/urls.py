from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop_drf'
urlpatterns = [
    path('products/', views.AllProducts.as_view() , name='AllProduts'),
    path('product/<int:pk>/', views.ProductDetail.as_view() , name='ProductDetail'),
    path('category/',views.AllCategories.as_view())

    # path('<int:product_id>/', views.ProductDetail.as_view() , name='ProductDetail'),
    # path('comment/', views.AddComment.as_view() , name='AddComment'),
    # path('like/<int:product_id>/', views.PostLike.as_view() , name='PostLike'),
    # path('<int:product_id>/', views.PostLike.as_view() , name='PostLike'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)