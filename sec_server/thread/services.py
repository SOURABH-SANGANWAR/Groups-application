from .models import MessageThread
from .serializers import MessageThreadSerializer,ThreadSerializer
from message.serializers import MessageSerializer
from message.models import Message
from message.services import MessageService
from rest_framework import status

# def get_group_messages(group_id, request):
#     messages = Message.objects.filter(thread__group__id=group_id)

class ThreadService:

    def get_thread(self, request, id):
        try:
            obj = MessageThread.objects.get(id=id)
            ser = MessageThreadSerializer(obj)
            data = ser.data
            return {'data':data,'errors':None}, status.HTTP_200_OK
        except Exception as e:
            return {'data':None,'errors':str(e)}, status.HTTP_400_BAD_REQUEST
    
    def get_threads(self, request, group_id):
        try:
            obj = MessageThread.objects.filter(group__id=group_id)
            ser = ThreadSerializer(obj, many=True)
            data = ser.data
            return {'data':data,'errors':None}, status.HTTP_200_OK  
        except Exception as e:
            return {'data':None,'errors':str(e)}, status.HTTP_400_BAD_REQUEST
        
    def create_thread(self, request, group_id):
        new_data = {}
        new_data['subject'] = request.data['subject']
        new_data['created_by'] = request.user.id
        new_data['updated_by'] = request.user.id
        new_data['group'] = group_id
        ser = ThreadSerializer(data=new_data)
        if ser.is_valid():
            obj = ser.save()
            print("Thread created with id: ", obj.id)
            service = MessageService()
            response,err_msg, msg_id = service.create_message(request, obj, request.FILES.getlist('files'), request.data['message'], request.user, None, None)
            if response:
                return obj.id
            else:
                raise Exception(err_msg)
        else:
            raise Exception(ser.errors)