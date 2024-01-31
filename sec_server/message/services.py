from .models import Message, MessageAttachment
from .serializers import MessageSerializer, MessageAttachmentSerializer
from rest_framework import status

class MessageService:
    def get_message(self, request, id):
        """
        This function is used to get a message by id.
        
        Parameters:
            request: request object
            id: id of the message
        
        Returns:
            data: message data"""
        try:
            obj = Message.objects.get(id=id)
            ser = MessageSerializer(obj)
            data = ser.data
            return {'data':data,'errors':None}, status.HTTP_200_OK
        except Exception as e:
            return {'data':None,'errors':str(e)}, status.HTTP_400_BAD_REQUEST
    

    def create_message_request(self, request, parent_id):
        """
        This function is used to create a new message.
        
        Parameters:
            request: request object
            parent_id: id of the parent message
            
        Returns:
            response: response object
            """
        parent = Message.objects.get(id=parent_id)
        try:
            message = request.data['message']
        except:
            raise Exception("Message is required")
        try:
            recieved_by = request.data['recieved_by']
        except:
            recieved_by = None
        try:
            files = request.FILES.getlist('files')
        except:
            files = None
        print(files)
        response, err_msg,msg_id = self.create_message(request = request, 
                                                thread = parent.thread, 
                                                files = files, 
                                                message=message, 
                                                sent_by = request.user, 
                                                recieved_by = recieved_by, 
                                                parent = parent
                                                )
        if response:
            return self.get_message(request, msg_id)
        else:
            raise Exception(err_msg)
        
        
    def create_message(self, request, thread, files, message, sent_by, recieved_by, parent):
        """
        This function is used to create a new message.
        
        Parameters:
            request: request object
            thread: thread object
            files: list of files from request
            message: message
            sent_by: user object who sent the message
            recieved_by: user object who recieved the message
            parent: parent message object
            
        Returns:
            response: response object
            """
        try:
            obj = Message.objects.create(thread=thread, message=message, sent_by=sent_by, recieved_by=recieved_by, parent=parent)
            obj.save()
            print("Message created with id: ", obj.id)
            print("Files: ", files)
            obj.create_attachments(files)
            print("Attachments created")
            return True,None,obj.id
        except Exception as e:
            print("not successful")
            return False,str(e),None
    
    # def delete_message(self, request, id):
    #     try:
    #         obj = Message.objects.get(id=id)
    #         obj.delete()
    #         return {'data':None,'errors':None}
    #     except Exception as e:
    #         return {'data':None,'errors':str(e)}
