from django.db import models
from group.models import Group
from usercustom.models import CustomUser
import uuid
# Create your models here.


class MessageThread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_threads')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='message_threads')
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='updated_message_threads', null=True, blank=True)