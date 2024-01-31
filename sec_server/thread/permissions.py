from member.models import GroupMember
from thread.models import MessageThread
def can_view_thread(user, thread_id):
    """
    User with access can view thread
    """
    try:
        thread = MessageThread.objects.get(id=thread_id)
        return GroupMember.objects.filter(user=user, group=thread.group).exists()
    
    except Exception as e:
        print(e)
        return False

def can_view_grp_messages(user, group_id):
    """
    User with access can view messages in group
    """
    try:
        return GroupMember.objects.filter(user=user, group__id=group_id).exists()
    except Exception as e:
        print(e)
        return False
