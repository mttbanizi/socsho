from rest_framework import serializers

from accounts.models import User, Relation


class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if validateEmail(email_or_username):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs



class GetUsernameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('pk','full_name')
        read_only_fields = ('pk','full_name')

class GetMyProfileSerializer(serializers.ModelSerializer):
    # accepted_following_count=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('pk','full_name','bio','status','follower_count','following_count')
        read_only_fields = ('pk','full_name','bio','status','follower_count', 'following_count')

    # def get_accepted_following_count(self,obj):
    #     queryset=obj.following.all()
    #     return AcceptedFollowingSerializer(instance=queryset)


# class AcceptedFollowingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Relation
#         fields=('pk','from_user', 'to_user', 'accepted')