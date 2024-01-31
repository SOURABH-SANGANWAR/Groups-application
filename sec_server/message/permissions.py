from member.models import GroupMember
from .models import Message

def can_get_message(user, message_id):
    """
    Checks if the user can manage roles of the group.
    """
    try:
        mes = Message.objects.get(id=message_id)
        print(mes.thread.group)
        return GroupMember.objects.get(user=user, group=mes.thread.group) != None
    except Exception as e:
        return False