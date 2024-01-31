from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django_filters import rest_framework as filters
from django.db import transaction
from .models import GroupMember
from .serializers import *
from .services import *
from rest_framework.pagination import PageNumberPagination
from .permissions import *
class GroupMemberView(generics.ListAPIView):
    """
    View to create a thread in the system.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = MemberSerializer
    filterset_class = filters.FilterSet
    search_fields = ['user__name', 'group__name', 'user__email']
    pagination_class = PageNumberPagination


    def get_serializer_context(self):
        """
        Method to add request object to serializer context."""
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context
    

    def get_queryset(self):
        """
        To list all members of a group."""
        group_id = self.kwargs['group_id']
        return GroupMember.objects.filter(group__id=group_id)
    
    def get(self, request, *args, **kwargs):
        """
        To list all members of a group.
        url:
        /group/<group_id>/ - GET"""
        if is_user_member_manager(request.user.id, kwargs['group_id']):
            return super().get(request, *args, **kwargs)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def post(self, request, group_id):
        """
        To invite a member to a group.
        url:
        /group/<group_id>/ - POST
        """
        if is_user_member_manager(request.user.id, group_id):
            try:
                with transaction.atomic():
                    serv = MemberServices()
                    response = serv.invite_member(request, group_id)
                    return Response(response, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)
        

class GetGroupMember(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = MemberSerializer
    filterset_class = filters.FilterSet
    search_fields = ['user__name', 'group__name', 'user__email']
    pagination_class = PageNumberPagination

    def get(self, request, group_id, member_id):
        """
        View method to get a member of a group.
        url:
        /group/get/<group_id>/<member_id>/ - GET
        """
        if is_user_member_manager(request.user.id, group_id):
            try:
                with transaction.atomic():
                    serv = MemberServices()
                    response = serv.get_member(request, group_id, member_id)
                    return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, group_id, member_id):
        """
        View method to update a member of a group.
        url:
        /group/get/<group_id>/<member_id>/ - PUT
        """
        if is_user_member_manager(request.user.id, group_id):
            try:
                with transaction.atomic():
                    serv = MemberServices()
                    response = serv.update_member(request, group_id, member_id)
                    return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, group_id, member_id):
        """
        View method to delete a member of a group.
        url:
        /group/get/<group_id>/<member_id>/ - DELETE
        """
        if is_user_member_manager(request.user.id, group_id):
            try:
                with transaction.atomic():
                    serv = MemberServices()
                    response = serv.delete_member(request, member_id)
                    return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)


class AcceptMember(APIView):
    """
    View class to accept a member request.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, group_id, member_id):
        """
        View method to accept a member request.
        url:
        /group/<group_id>/<member_id>/accept/ - PUT"""
        if is_user_member_manager(request.user.id, group_id):
            try:
                with transaction.atomic():
                    serv = MemberServices()
                    response = serv.accept_member(request, member_id)
                    return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':'You are not a manager of this group'}, status=status.HTTP_401_UNAUTHORIZED)


class JoinAsMember(APIView):
    """
    View class to join a group as a member.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, group_id):
        """
        View method to join a group as a member.
        url:
        /group/<group_id>/join/ - PUT
        """
        try:
            with transaction.atomic():
                serv = MemberServices()
                response = serv.join_as_member(request, group_id)
                return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)