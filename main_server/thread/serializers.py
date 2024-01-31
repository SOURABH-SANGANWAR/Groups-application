from rest_framework import serializers
from .models import MessageThread
from message.serializers import MessageSerializer


class MessageThreadSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    messages = serializers.SerializerMethodField('get_messages', read_only=True)

    def get_messages(self, obj):
        messages = obj.message_set.all()
        # sent_queryset = messages.filter(sent_by=self.context['request'].user)
        # recieved_queryset = messages.filter(recieved_by=self.context['request'].user)
        # recieved_by_all_queryset = messages.filter(recieved_by__isnull=True)
        # thread_messages = sent_queryset | recieved_queryset | recieved_by_all_queryset
        thread_messages = messages
        return MessageSerializer(thread_messages, many=True).data



    class Meta:
        model = MessageThread
        fields = [ 'subject', 'group_name', 'updated_at', 'updated_by', 'id', 'messages']

class ThreadSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = MessageThread
        fields = [ 'subject', 'group_name', 'group', 'updated_at', 'updated_by', 'id', 'created_by', 'created_at']

        kwargs = {
            'updated_at': {
                'read_only': True
            },
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            },
        }