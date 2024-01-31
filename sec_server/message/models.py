from django.db import models
from group.models import Group
from thread.models import MessageThread
from member.models import GroupMember
import datetime
import uuid
from usercustom.models import CustomUser
# Create your models here.

# CREATE TABLE messages (
#     id SERIAL PRIMARY KEY,
#     group_id INTEGER NOT NULL REFERENCES groups(id),
#     message_id VARCHAR(255) NOT NULL,
#     subject VARCHAR(255) NOT NULL,
#     body TEXT NOT NULL,
#     sender_id INTEGER NOT NULL REFERENCES users(id),
#     thread_id INTEGER REFERENCES messages(id),
#     parent_id INTEGER REFERENCES messages(id),
#     children INTEGER[] NOT NULL DEFAULT '{}',
#     receiver_id INTEGER NOT NULL REFERENCES users(id),
#     level INTEGER NOT NULL DEFAULT 0,
#     is_thread_starter BOOLEAN NOT NULL DEFAULT FALSE
# );

def get_upload_path(instance, filename):
    timestamp = datetime.datetime.now().timestamp()
    return f'message_attachments/{instance.message.id}/{timestamp}_{filename}'

class MessageAttachment(models.Model):
    file = models.FileField(upload_to=get_upload_path)
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='attachments')

    def get_file_name(self):
        return self.file.name.split('/')[-1]
    
    def __str__(self):
        return self.file.name

class Message(models.Model):
    """
    This class is a model for a message. Message is a part of a thread.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE, related_name='message_set')
    sent_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    sent_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    recieved_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recieved_messages', blank=True, null=True)
    
    def __str__(self):
        return self.message[:20] + ' - ' + self.thread.subject
    
    def get_attachments(self):
        return self.attachments.all()
    
    def create_attachments(self, files):
        for i in files:
            obj = MessageAttachment.objects.create(message=self, file=i)
            obj.save()
