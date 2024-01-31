from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import MessageThread
from rest_framework import generics
from .serializers import *
from django_filters import rest_framework as filters
from .services import ThreadService
from rest_framework.pagination import PageNumberPagination
from group.models import Group 
# import django atomic
from django.db import transaction
from .permissions import *


class ThreadDetailView(APIView):
    """
    View to create a thread in the system.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        """
        View to get a thread in the system.
        
        url:
        /thread/<id>/ - GET"""
        if can_view_thread(request.user, id):
            ts = ThreadService()
            data,status_data = ts.get_thread(request, id)
            return Response(data, status=status_data)
        else:
            return Response({'data':None,'errors':'You are not a member of this group'}, status=status.HTTP_401_UNAUTHORIZED)



class ThreadView(generics.ListAPIView):
    """
    View to create a thread in the system.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ThreadSerializer
    filterset_class = filters.FilterSet
    search_fields = ['name', 'description', 'email']
    pagination_class = PageNumberPagination


    def get_serializer_context(self):
        """
        Method to add request object to serializer context."""
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context

    def get_queryset(self):
        """
        To list all threads in a group."""
        group_id = self.kwargs['group_id']
        return MessageThread.objects.filter(group__id=group_id)
    
    def get(self, request, *args, **kwargs):
        """
        View list all threads in a group.
        url:
        /thread/group/<group_id>/ - GET
        """
        if can_view_grp_messages(request.user, kwargs['group_id']):
            return super().get(request, *args, **kwargs)
        else:
            return Response({'data':None,'errors':'You are not a member of this group'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, group_id):
        """
        View to create a thread in the system.
        
        url:
        /thread/group/<group_id>/ - POST
        
        request:
        {
            "subject": "subject",
            "message": "message",
            "files": [Files_attachments],
        }"""
        if can_view_grp_messages(request.user, group_id):
            try:
                with transaction.atomic():
                    ts = ThreadService()
                    new_thread = ts.create_thread(request, group_id)
                    response,status_data = ts.get_thread(request, new_thread)
                    print(response , status_data, "responsefro " )
                    return Response(response, status=status_data)
            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':'You are not a member of this group'}, status=status.HTTP_401_UNAUTHORIZED)
