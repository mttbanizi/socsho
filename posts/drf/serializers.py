from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    #image = serializers.ImageField(required=False)
    comments=serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('pk','user','created','body','slug','image','comments')
        read_only_fields = ('pk','user','created','slug')

    def get_comments(self,obj):
        result = obj.pcomment.all()
        return PostCommentsSerializers(instance=result, many=True).data

class PostCommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk','body','user','created')
        read_only_fields = ('pk','user','created')
