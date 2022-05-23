from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
#from permissions import IsOwnerOrReadOnly

from .serializers import PostSerializer
from posts.models import Post


class AllPosts(APIView):
    def get(self, request):
        queryset=Post.objects.all()
        print(50*'*')
        print (queryset)
        serializer=PostSerializer(queryset, many=True)
        return Response(serializer.data)


