from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('body', 'slug', 'user', 'created')

    

