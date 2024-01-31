from rest_framework import serializers
from .models import Message, MessageAttachment
from member.models import GroupMember

class MessageAttachmentSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField('get_file_name')
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file_name']
    
    def get_file_name(self, obj):
        return obj.get_file_name()

class MessageSerializer(serializers.ModelSerializer):
    Attachments = MessageAttachmentSerializer(many=True, read_only=True, source = 'attachments')
    sent_by = serializers.CharField(source='sent_by.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'message', 'thread', 'sent_by', 'sent_at', 'parent', 'recieved_by', 'Attachments']

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        message.sent_by = GroupMember.objects.get(user=self.context['request'].user)
        return message