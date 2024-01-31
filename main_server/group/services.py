from .models import Group
from permissions.models import RolePermission
from member.models import GroupMember
from .serializers import GroupSerializer
from rest_framework import status

basic_role = {}
basic_role['role_name'] = 'member'
basic_role['role_description'] = 'Basic role for all members'
basic_role['is_default'] = True

admin_rol = {}
admin_rol['role_name'] = 'admin'
admin_rol['role_description'] = 'Admin role for all members'
admin_rol['is_default'] = False
admin_rol['post_as_group'] = True
admin_rol['manage_members'] = True
admin_rol['manage_content'] = True
admin_rol['manage_metadata'] = True
admin_rol['can_post'] = True
admin_rol['manage_roles'] = True
admin_rol['reply_to_authors'] = True
admin_rol['attach_files'] = True
admin_rol['view_member_email_addresses'] = True

def create_group(request):
    global basic_role, admin_rol
    """
    Creates a group.

    Parameters:
        request (Request): The request object

    Returns:
        dict: A dictionary containing the data and errors if any.
        status: The status code.
    """
    try:
        print("creating group")
        ser = GroupSerializer(data=request.data, context={'request':request})
        if ser.is_valid():
            print("valid")
            ser.save()
            print("saved")
            print("creating role 1")
            mem_role = RolePermission.objects.create(**basic_role, group=ser.instance)
            print("saving role 1")
            mem_role.save()
            print("creating role 2")
            admin_role = RolePermission.objects.create(**admin_rol, group=ser.instance)
            print("saving role 2")
            admin_role.save()
            print("roles saved")
            mem = GroupMember.objects.create(user=request.user, group=ser.instance, role=admin_role, username = request.user.username, email_id = request.user.email)
            print("member created")
            mem.save()
            print("member saved")
            return {'data':ser.data,'errors':None}, status.HTTP_201_CREATED
        else:
            print("invalid")
            print(ser.errors)
            raise Exception(ser.errors)
    except Exception as e:
        print("exception")
        print(e)
        try:
            GroupMember.objects.using(ser.instance.db_region).get(id = mem.id).delete()
        except Exception as x:
            print(x)
        try:
            RolePermission.objects.using(ser.instance.db_region).get(id = mem_role.id).delete()
        except Exception as x:
            print(x)
        try:
            RolePermission.objects.using(ser.instance.db_region).get(id = admin_role.id).delete()
        except Exception as x:
            print(x)
        try:
            Group.objects.using(ser.instance.db_region).get(id = ser.instance.id).delete()
        except Exception as x:
            print(x)
        print(e)
        raise e