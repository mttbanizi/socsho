from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
#from permissions import IsOwnerOrReadOnly
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer, CategorySerializer, ProductDetailSerializer
from shop.models import Product, ProductImage, Category,ProductSpecification, ProductSpecificationValue
from posts.models import Post


class AllCategories(APIView):

    def get(self, request):
        categories=Category.objects.all()
        srz_data=CategorySerializer(instance=categories, many=True)
        return Response(srz_data.data)


class AllProducts(APIView):

    def get(self, request):
        products=Product.objects.all()
        srz_data=ProductSerializer(instance=products,many=True)
        return Response(srz_data.data)

    def post(self, request):
        queryset = Product.objects.all()
        parser_classes = [MultiPartParser, FormParser]
        permission_classes = [IsAuthenticated,]
        srz_data = ProductSerializer(data=request.data)
        if srz_data.is_valid():
            slug = slugify(request.data['description'][:30], allow_unicode=True)
            product=srz_data.save(user=request.user, slug=slug)
            try:
                # try to get and save images (if any)
                images_data = dict((request.FILES).lists()).get('images', None)
                is_feature=True
                for image in images_data:
                    ProductImage.objects.create(product=product, image=image,is_feature=is_feature)
                    is_feature=False
            except:
                # if no images are available - create using default image
                
                ProductImage.objects.create(product=product)
            specc_list=ProductSpecification.objects.filter(category=request.data['category'])
            for sp in specc_list:
                print(10*'-pNme--')
                print(sp.name)
                if sp.name in request.data:
                    specification_value=request.data[sp.name]
                    print(10*'spNme--')
                    print(sp.name)
                    ProductSpecificationValue.objects.create(product=product, specification=sp, value=specification_value)

                    

            post=Post.objects.create(user=request.user, body=request.data['description'], slug = slug, image=image)

            return Response(srz_data.data, status=status.HTTP_201_CREATED)   
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        srz_data=ProductDetailSerializer(instance=product)
        return Response(srz_data.data)
