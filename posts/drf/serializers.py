from accounts.models import User, ProfilePhoto
from rest_framework import serializers

from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    #image = serializers.ImageField(required=False)
    comments=serializers.SerializerMethodField()
    user_fields=serializers.SerializerMethodField()
   


    class Meta:
        model = Post
        fields = ('pk','user','created','body','slug','image','comments','user_fields')
        read_only_fields = ('pk','user','created','slug')

    def get_comments(self,obj):
        result = obj.pcomment.all()
        return PostCommentsSerializers(instance=result, many=True).data

    def get_user_fields(self,obj):
        result=obj.user
        return PostUserSerializers(instance=result).data

    

class PostCommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk','body','user','created')
        read_only_fields = ('pk','user','created')

      
    
class PostUserSerializers(serializers.ModelSerializer):
    user_photo=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields=('pk','full_name','user_photo')
        read_only_fields = ('pk','full_name')

    def get_user_photo(self,obj):
        result=obj.uprofilephoto.all()
        return UserProfilePhoto(instance=result,many=True).data

class UserProfilePhoto(serializers.ModelSerializer):
    class Meta:
        model=ProfilePhoto
        fields=('image',)
