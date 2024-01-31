from rest_framework import serializers
from .models import CustomUser
from django.conf import settings
from otpdetails.models import Otpdetails
class UserSerializer(serializers.ModelSerializer):

    """
    This serializer is used to serialize the user model.
    """
    Profile_picture = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    def get_Profile_picture(self, obj):
        if obj.profile_picture:
            return f'{settings.HOSTNAME}:{settings.PORT}{obj.profile_picture.url}'
        else:
            return None
    class Meta:
        model = CustomUser 
        fields = ('id', 'username', 'email', 'password', 'profile_picture', 'Profile_picture', 'is_activated', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'id': {
                'read_only': True
            },
            'is_activated': {
                'read_only': True
            }
        }
    
    def create(self, validated_data):
        """
        This function is used to create a new user.
        
        Parameters:
            validated_data (dict): The validated data from the serializer.
        
        Returns:
            CustomUser: The created user.
            """
        user = CustomUser.objects.create_user(**validated_data)
        user.save()
        otp = Otpdetails.objects.create(user=user)
        otp.setup()
        otp.save()
        return user

class ListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the user model.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UpdateSerializer(serializers.ModelSerializer):
    Profile_picture = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    def get_Profile_picture(self, obj):
        if obj.profile_picture:
            return f'{settings.HOSTNAME}:{settings.PORT}{obj.profile_picture.url}'
        else:
            return None
        
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'profile_picture', 'Profile_picture')
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'profile_picture': {
                'required': False
            },
            'Profile_picture': {
                'read_only': True
            }
        }