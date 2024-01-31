from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django_filters import rest_framework as filters
from django.db import transaction
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from .permissions import *


class RolePermissionView(generics.ListAPIView):
    """
    View to create a new role in group and list types of roles
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = RolePermissionSerializer
    filterset_class = filters.FilterSet
    search_fields = ['role_name', 'description']
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        """
        Method to add request object to serializer context."""
        cont =  super().get_serializer_context()
        cont.update({'request':self.request})
        return cont
    
    def get_queryset(self):
        """
        To list all roles in a group."""
        group_id = self.kwargs['group_id']
        return RolePermission.objects.filter(group__id=group_id)
    
    def get(self, request, *args, **kwargs):
        """
        View list all roles in a group.
        url:
        /role/group/<group_id>/ - GET"""
        if can_manage_roles(request.user.id, kwargs['group_id']):
            return super().get(request, *args, **kwargs)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, group_id):
        """
        View to create a new role in group.
        url:
        /role/group/<group_id>/ - POST
        """
        if can_manage_roles(request.user.id, group_id):
            try:
                temp_data = request.data.copy()
                temp_data['group'] = group_id
                ser = RolePermissionSerializer(data=temp_data)
                if ser.is_valid():
                    ser.save()
                    return Response({'data':ser.data,'errors':None}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'data':None,'errors':ser.errors}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)
        

class RolePermissionDetailView(APIView):
    """
    View to create a new role in group and list types of roles
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, group_id, id):
        """
        View to get details of a role in group.
        url:
        /role/<group_id>/<id>/ - GET
        """
        if can_manage_roles(request.user.id, group_id):
            try:
                role = RolePermission.objects.filter(group__id = group_id).get(id=id)
                ser = RolePermissionSerializer(role)
                return Response({'data':ser.data,'errors':None}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def put(self, request, group_id, id):
        """
        View to update details of a role in group.
        url:
        /role/<group_id>/<id>/ - PUT
        """
        if(can_manage_roles(request.user.id, group_id) == False):
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            temp_data = request.data.copy()
            temp_data['group'] = group_id
            role = RolePermission.objects.filter(group__id = group_id).get(id=id)
            ser = RolePermissionSerializer(role, data=temp_data)
            if ser.is_valid():
                ser.save()
                return Response({'data':ser.data,'errors':None}, status=status.HTTP_200_OK)
            return Response({'data':None,'errors':ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, group_id, id):
        """
        View to delete a role in group.
        url:
        /role/<group_id>/<id>/ - DELETE
        """
        if(can_manage_roles(request.user.id, group_id) == False):
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            role = RolePermission.objects.filter(group__id = group_id).get(id=id)
            role.delete()
            return Response({'data':None,'errors':None}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)