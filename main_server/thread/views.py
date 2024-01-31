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


class ThreadDetailView(APIView):
    def get(self, request, id):
        ts = ThreadService()
        data,status_data = ts.get_thread(request, id)
        return Response(data, status=status_data)



class ThreadView(generics.ListAPIView):
    """
    View to create a thread in the system.
    """
    # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ThreadSerializer
    filterset_class = filters.FilterSet
    search_fields = ['name', 'description', 'email']
    pagination_class = PageNumberPagination


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return MessageThread.objects.filter(group__id=group_id)
    
    def post(self, request, group_id):
        try:
            with transaction.atomic():
                ts = ThreadService()
                new_thread = ts.create_thread(request, group_id)
                response,status_data = ts.get_thread(request, new_thread)
                return Response(response, status=status_data)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
