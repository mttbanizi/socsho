from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
#from permissions import IsOwnerOrReadOnly
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer, ProductImageSerializer
from shop.models import Product, ProductImage


class AllProduts(APIView):

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
            # product = Product.objects.filter(user=request.user).last()
            try:
                # try to get and save images (if any)
                images_data = dict((request.FILES).lists()).get('images', None)
                print(10*'Images---')
                print (images_data)
                print (product)
                for image in images_data:
                    ProductImage.objects.create(product=product, image=image)
            except:
                # if no images are available - create using default image
                
                ProductImage.objects.create(product=product)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)   
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)