from rest_framework import serializers
from .models import RolePermission

class RolePermissionSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the role permission model."""
    class Meta:
        model = RolePermission
        fields = '__all__'

    def create(self, validated_data):
        """
        This serializer method to create role permission."""
        obj = super(RolePermissionSerializer,self).create(validated_data)
        return obj
    
    def update(self, instance, validated_data):
        obj = super(RolePermissionSerializer,self).update(instance, validated_data)
        return obj