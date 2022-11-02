from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer

#from permissions import IsOwnerOrReadOnly
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from accounts.models import User

from .serializers import GetUsernameSerializer,AuthCustomTokenSerializer


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        FormParser,
        MultiPartParser,
        JSONParser,
    )

    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': unicode(token.key),
        }

        return Response(content)


class GetUsername(APIView):

    #  permission_classes = [IsAuthenticated,]
    permission_classes = [IsAuthenticated,]
    def get(self, request,user_id):
        queryset=get_object_or_404(User,pk=user_id)
        serializer=GetUsernameSerializer(queryset)
        return Response(serializer.data)
