from rest_framework.serializers import ModelSerializer

from django.utils.text import slugify


from shop.models import Product, ProductImage


# class ProductSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('pk','user','created_at','category', 'title', 'description','price','discount_price','slug')
#         read_only_fields = ('pk','user','created','slug')


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product']
        extra_kwargs = {
        'product': {'required': False},
        }

class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id','user', 'title', 'description', 'images', 'price', 'discount_price', 'is_active', 'category', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['id','user','slug','created_at', 'updated_at',  'is_active']
        #lookup_field = 'slug'
