from rest_framework import serializers
from .models import Message, MessageAttachment
from member.models import GroupMember

class MessageAttachmentSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the message attachment model.
    """
    file_name = serializers.SerializerMethodField('get_file_name')
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file_name']
    
    def get_file_name(self, obj):
        """
        This function is used to get the file name of the attachment."""
        return obj.get_file_name()

class MessageSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the message model.
    """
    Attachments = MessageAttachmentSerializer(many=True, read_only=True, source = 'attachments')
    sent_by = serializers.CharField(source='sent_by.username', read_only=True)
    email = serializers.CharField(source='sent_by.email', read_only=True)
    profile_picture = serializers.CharField(source='sent_by.profile_picture', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'message', 'thread', 'sent_by', 'sent_at', 'parent', 'recieved_by', 'Attachments', 'email', 'profile_picture']

    def create(self, validated_data):
        """
        This function is used to create a new message.
        """
        message = Message.objects.create(**validated_data)
        message.sent_by = GroupMember.objects.filter(user=self.context['request'].user).get(group=message.thread.group)
        message.save()
        return message