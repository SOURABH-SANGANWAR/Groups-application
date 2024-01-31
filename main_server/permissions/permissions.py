from member.models import GroupMember

def can_manage_roles(user_id, group_id):
    """
    Checks if the user can manage roles of the group.
    """
    try:
        return GroupMember.objects.get(user__id=user_id, group__id=group_id).role.manage_roles
    except Exception as e:
        return False