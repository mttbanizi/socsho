
# from urllib import 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
#from permissions import IsOwnerOrReadOnly
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer, PostCommentsSerializers
from posts.models import Comment, Post, Vote


class AllPosts(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        queryset=Post.objects.all()
        serializer=PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        parser_classes =[MultiPartParser, FormParser]
        srz_data =PostSerializer(data=request.data)
        if srz_data.is_valid():
            slug = slugify(request.data['body'][:30], allow_unicode=True)
            srz_data.save(user=self.request.user, slug=slug)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request,post_id):
        queryset=Post.objects.filter(pk=post_id)
        serializer=PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self,request, post_id):
        queryset=Post.objects.get(pk=post_id)
        if request.user == queryset.user :
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, post_id):
        parser_classes =[MultiPartParser, FormParser]
        post=Post.objects.get(pk=post_id)
        srz_data = PostSerializer(instance=post, data=request.data, partial=True)
        if srz_data.is_valid():
            if srz_data.validated_data.get('body',None):
                slug = slugify(srz_data.validated_data['body'], allow_unicode=True)
                srz_data.save(slug=slug)
                return Response(srz_data.data, status=status.HTTP_200_OK)
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class AddComment(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self,request):
        post=Post.objects.get(pk=request.data['post_id'])
        serializer=PostCommentsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        comment=Comment.objects.get(pk=request.data['comment_id'])
        if request.user == comment.user :
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        comment=Comment.objects.get(pk=request.data['comment_id'])
        srz_data = PostCommentsSerializers(instance=comment, data=request.data, partial=True)
        if srz_data.is_valid():
            if srz_data.validated_data.get('body',None):
                slug = slugify(srz_data.validated_data['body'], allow_unicode=True)
                srz_data.save(slug=slug)
                return Response(srz_data.data, status=status.HTTP_200_OK)
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class AddReply(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self,request):
        comment=Comment.objects.get(pk=request.data['comment_id'])
        serializer=PostCommentsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,post=comment.post, reply=comment, is_reply=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLike(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self,request,post_id):
        vote=Vote.objects.filter(post__id=post_id, user=request.user).last()
        if vote:
            return Response({'liked':'like'}, status=status.HTTP_200_OK)
        return Response({'liked':'dislike'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote(post=post, user=request.user)
        if like:
            like.save()
            return Response({'liked':'like'}, status=status.HTTP_200_OK)
        return Response( status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,post_id):
        post = get_object_or_404(Post, id=post_id)
        Vote.objects.filter(post=post, user=request.user).delete()
        return Response({'liked':'dislike'}, status=status.HTTP_200_OK)





