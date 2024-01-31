from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Message
from rest_framework import generics
from .serializers import MessageSerializer
from django_filters import rest_framework as filters
from django.http import HttpResponse
from .services import MessageService
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .permissions import *

class messageView(APIView):
    def get(self, request, id):
        """
        View to get a message in the system.
        url:
        /message/id/ -GET
        """
        if can_get_message(request.user, id):
            try:
                obj = Message.objects.get(id=id)
                ser = MessageSerializer(obj)
                return Response({'data':ser.data,'errors':None}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None,'errors':"You are not allowed to view this message."}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, id):
        """
        View to reply to a message in the system.
        url:
        /message/id/ -POST
        """
        if not can_get_message(request.user, id):
            return Response({'data':None,'errors':"You are not allowed to view this message."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            with transaction.atomic():
                service = MessageService()
                response, status_data = service.create_message_request(request, id)
                return Response(response, status=status_data)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        """
        View to reply to author.
        url:
        /message/id/ -PUT
        """
        if not can_get_message(request.user, id):
            return Response({'data':None,'errors':"You are not allowed to view this message."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            message = request.data.get('message')
            obj = Message.objects.get(id=id)
            username = obj.sent_by.username
            user_email = obj.sent_by.email
            email_by = request.user.email
            email_username = request.user.username
            subject = f"Reply to {obj.thread.subject} in Groups website"
            message = f"Hi {username},\nThis is a reply email by {email_username}<{email_by}>\nGroup name: {obj.thread.group.name}\nSubject :{obj.thread.subject}\n{message}\n\nThanks,\n{email_username}"
            if obj.thread.group.is_email_validated:
                email_id = obj.thread.group.email
                email_password = obj.thread.group.email_password
                send_mail(subject, message, email_by, [user_email,email_by], fail_silently=True, auth_user=email_id, auth_password=email_password)
            else:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email,email_by], fail_silently=True)
            return Response({'data':"email sent.",'errors':None}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)


        
class GetAttachment(APIView):
    def get(self, request, id, attach_id):
        """
        View to get attachment of a message in the system.
        url:
        /message/attachment/id/attach_id -GET
        """
        try:
            obj = Message.objects.get(id=id)
            print("attachments: ", obj.attachments.all())
            attach_file = obj.attachments.get(id=attach_id)
            response = HttpResponse(attach_file.file, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="%s"' % attach_file.get_file_name()
            return response
        except Exception as e:
            return Response({'data':None,'errors':str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class ReplyAll(APIView):
#     def post(self, request, id):
#         try:
#             obj = Message.objects.get(id=id)
#             new_data = request.data.copy()
#             new_data['parent'] = obj.id
#             new_data['thread'] = obj.thread.id
#             new_data['sent_by'] = request.user.id
