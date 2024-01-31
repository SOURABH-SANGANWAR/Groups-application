from rest_framework import serializers
from .models import GroupMember
from usercustom.serializers import UserSerializer
from permissions.serializers import RolePermissionSerializer

class MemberSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the group member model.
    """
    Role = RolePermissionSerializer(read_only=True, source = 'role')

    class Meta:
        model = GroupMember
        fields = ['id', 'group', 'user', 'is_pending', 'is_invited', 'Role', 'role', 'email_id', 'username', 'profile_picture']

        kwargs = {
            'created_at': {
                'read_only': True
            },
            'updated_at': {
                'read_only': True
            }
        }
    
    def create(self, validated_data):
        """
        This serializer method to create group member.
        """
        obj = super(MemberSerializer, self).create(validated_data)
        if obj.user:
            obj.save(email_id = obj.user.email, username = obj.user.username, profile_picture = obj.user.profile_picture)
        return obj
    
    def update(self, instance, validated_data):
        """
        This serializer method to update group member.
        """
        obj = super(MemberSerializer, self).update(instance, validated_data)
        if obj.user:
            obj.save(email_id = obj.user.email, username = obj.user.username, profile_picture = obj.user.profile_picture)
        return obj
    