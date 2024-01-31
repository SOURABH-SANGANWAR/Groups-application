from .models import Group
from rest_framework import serializers
from django.conf import settings
import datetime
from member.serializers import MemberSerializer
from member.models import GroupMember
from django.conf import settings

class GroupSerializer(serializers.ModelSerializer):

    """
    This serializer is used to serialize the group model.
    """
    profile_image = serializers.ImageField(required=False, allow_null=True)
    Profile_image = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()
    host_website = serializers.SerializerMethodField() 

    def get_member(self, obj):
        """
        This serializer method to get member.
        """
        user = self.context['request'].user
        if user == None:
            return {}
        member_ser = MemberSerializer(GroupMember.objects.filter(group=obj).get(user__id=user.id))
        return member_ser.data
    
    def get_host_website(self, obj):
        """
        This serializer method to get host website.
        """
        return settings.SECONDARY_HOSTS[obj.db_region]


    def get_Profile_image(self, obj):
        """
        This serializer method to get profile image url.
        """
        if obj.profile_image:
            return f'{settings.HOSTNAME}:{settings.PORT}{obj.profile_image.url}'
        else:
            return None

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'is_public_view', 'is_public_join', 'email', 'email_password', 'is_email_validated', 'profile_image','Profile_image', 'db_region', 'created_by', 'updated_by', 'member', 'host_website']
        extra_kwargs = {
            'email_password': {
                'write_only': True
            },
            'is_email_validated': {
                'read_only': True
            },
            'created_by': {
                'read_only': True
            },
            'updated_by': {
                'read_only': True
            }
        }
    
    def create(self, validated_data):
        """
        This serializer method to create group.
        """
        val_data = validated_data.copy()
        print("creating")
        val_data['created_by'] = self.context['request'].user
        val_data['updated_by'] = self.context['request'].user
        obj = super().create(val_data)
        if 'email' in self.context['request'].data:
            if 'email_password' in self.context['request'].data:
                obj.email_password = self.context['request'].data['email_password']
                obj.email = self.context['request'].data['email']
        obj.is_email_validated = False
        obj.save()
        return obj
    
    def update(self, instance, validated_data):
        """
        This serializer method to update group.
        """
        obj = super().update(instance, validated_data)
        obj.updated_by = self.context['request'].user
        obj.updated_at = datetime.datetime.now()
        if 'email' in self.context['request'].data:
            if 'email_password' in self.context['request'].data:
                obj.email_password = self.context['request'].data['email_password']
                obj.email = self.context['request'].data['email']
        obj.save()
        return obj
    
    def delete(self, instance):
        """
        This serializer method to delete group.
        """
        instance.soft_delete(self.context['request'].user)
        return instance


class ListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the groups model. This is serializer for searching groups
    """
    Profile_image = serializers.SerializerMethodField()

    def get_Profile_image(self, obj):
        """
        This serializer method to get profile image url.
        """
        if obj.profile_image:
            return f'{settings.HOSTNAME}:{settings.PORT}{obj.profile_image.url}'
        else:
            return None

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'is_public_view', 'is_public_join', 'Profile_image']