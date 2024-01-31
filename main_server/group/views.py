from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Group
from rest_framework import generics
from .serializers import GroupSerializer, ListSerializer
from django_filters import rest_framework as filters
from django.db import transaction
from .services import create_group
from rest_framework.pagination import PageNumberPagination
from member.models import GroupMember
from .permissions import *
# Create your views here.
class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = ['name', 'description', 'is_public_join', 'email', 'is_email_validated']

class GroupsView(generics.ListAPIView):
    """
    View to create a group in the system or list public groups.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ListSerializer
    filterset_class = GroupFilter
    search_fields = ['name', 'description', 'email']
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        """
        Method to add request object to serializer context.
        """
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context

    def get_queryset(self):
        """
        To list public groups.
        """
        return Group.objects.filter(is_public_view=True)
    

    def post(self, request, *args, **kwargs):
        """
        This method creates groups.
        url:
        /group/ - POST
        """
        try:
            with transaction.atomic():
                response, stat = create_group(request)
                return Response(response, status=stat)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GroupsUserView(generics.ListAPIView):
    """
    View to list groups of current loggedIn user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupSerializer
    filterset_class = GroupFilter
    search_fields = ['name', 'description', 'email']
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context

    def get_queryset(self):
        """
        To list groups of current loggedIn user.
        """
        return Group.objects.filter(group_members__user__id = self.request.user.id)


class GroupView(generics.RetrieveUpdateDestroyAPIView):
    """
    This is Retrive update destroy view for group.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return super().get_object()

    def get(self,request, id, *args, **kwargs):
        """
        This method retrives group details.
        url:
        /group/<id>/ - GET
        Response:
        Json : {'data':<Json group data>, 'errors':<Error message>}
        """
        try:
            obj = Group.objects.get(id=id)
        except Exception as e:
            return Response({'data':None,'errors':"Invalid Group"}, status=status.HTTP_400_BAD_REQUEST)
        if can_view_group(request.user.id, obj):
            try:
                ser = GroupSerializer(obj, context={'request':request})
                return Response({'data':ser.data,'errors':None}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(request.user.username, Group.objects.get(id=id).name)
            return Response({'data':None,'errors':"You are not a member of this group"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, id, *args, **kwargs):
        """
        This method updates group details.
        url:
        /group/<id>/ - PUT
        Response:
        Json : {'data':<Json group data>, 'errors':<Error message>}
        """
        try:
            if is_group_admin(request.user.id, id):
                obj = Group.objects.get(id=id)
                ser = GroupSerializer(obj, data=request.data, context={'request':request})
                if ser.is_valid():
                    ser.save()
                    return Response({'data':ser.data,'errors':None}, status=status.HTTP_200_OK)
                else:
                    return Response({'data':None,'errors':ser.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'data':None,'errors':"You are not admin of this gorup"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        """
        This method deletes group.
        url:
        /group/<id>/ - DELETE
        Response:
        Json : {'data':<Json group data>, 'errors':<Error message>}
        """
        if is_group_admin(request.user.id, id):
            try:
                obj = Group.objects.get(id=id)
                ser = GroupSerializer(obj, context={'request':request})
                ser.delete(obj)
                return Response({'data':None,'errors':None}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':"You are not admin of this gorup"}, status=status.HTTP_401_UNAUTHORIZED)
    