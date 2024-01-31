from member.models import GroupMember


def is_user_member_manager(user_id, group_id):
    """
    Checks if the user is a manager of the group.
    """
    try:
        return GroupMember.objects.get(user__id=user_id, group__id=group_id).role.manage_members
    except Exception as e:
        return False