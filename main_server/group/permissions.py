from member.models import GroupMember

def is_group_admin(user_id, group_id):
    """
    Checks if the user is an admin of the group.

    Parameters:
        user_id (int): The id of the user.
        group_id (int): The id of the group.

    Returns:
        bool: True if the user is an admin of the group, False otherwise.
    """
    try:
        return GroupMember.objects.get(user__id=user_id, group__id=group_id).role.manage_metadata
    except Exception as e:
        return False
    
def can_view_group(user_id, group):
    """
    Checks if the user can view the group.

    Parameters:
        user_id (int): The id of the user.
        group (Group): The group object.
    
    Returns:
        bool: True if the user can view the group, False otherwise.
    """
    try:
        print("all mem : ", GroupMember.objects.all())
        return GroupMember.objects.filter(user__id=user_id, group__id=group.id).exists() or group.is_public_view
    except Exception as e:
        print("error ",str(e))
        return False
