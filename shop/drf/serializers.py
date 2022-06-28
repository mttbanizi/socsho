from itertools import product
from rest_framework.serializers import ModelSerializer,SerializerMethodField, StringRelatedField,Field
from rest_framework_recursive.fields import RecursiveField

from django.utils.text import slugify


from shop.models import Product, ProductImage,ProductSpecification, ProductSpecificationValue, Category


class CategorySerializer(ModelSerializer):
    children = RecursiveField(many=True, required=False)
    # full_name = SerializerMethodField("get_full_name")
    

    class Meta:
        model = Category
        fields = ('id', 'name', 'children')

    def get_full_name(self, obj):
        name = obj.name

        if "parent" in self.context:
            parent = self.context["parent"]

            parent_name = self.context["parent_serializer"].get_full_name(parent)

            name = "%s - %s" % (parent_name, name, )

        return name


class ProductSpecificationSerializer(ModelSerializer):
    class Meta:
        model= ProductSpecification
        fields=['category','name']


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product']
        

class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id','user', 'title', 'description', 'images', 'price', 'discount_price', 'is_active', 'category', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['id','user','slug','created_at', 'updated_at',  'is_active']
        #lookup_field = 'slug'


class ProductSpecificationValueSerializer(ModelSerializer):
    specification=StringRelatedField()
    class Meta:
        model=ProductSpecificationValue
        fields=['specification','value']


class ProductDetailSerializer(ModelSerializer):
    images = SerializerMethodField()
    atribute=SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','user', 'title', 'description', 'images', 'price','atribute', 'discount_price', 'is_active', 'category', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['id','user','slug','created_at', 'updated_at',  'is_active']


    def get_images(self,obj):
        images=ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(instance=images, many=True).data

    def get_atribute(self,obj):
        atrib=ProductSpecificationValue.objects.filter(product=obj)
        return ProductSpecificationValueSerializer(instance=atrib, many=True).data
