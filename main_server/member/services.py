from .models import GroupMember
from .serializers import MemberSerializer
from group.models import Group
from usercustom.models import CustomUser
from permissions.models import RolePermission


class MemberServices:

    def get_member(self, request, group_id, member_id):
        """
        User with access can get member details

        Parameters:
            request (request): request data
            group_id (uuid): group id
            member_id (uuid): member id
        
        Returns:
            dict: member data
        """
        member = GroupMember.objects.get(id=member_id)
        print("member : ", member)
        print("group id : ", group_id, " member group id : ", member.group.id)
        if str(member.group.id) == group_id:
            ser = MemberSerializer(member)
            return {'data':ser.data, 'errors':None}
        else:
            raise Exception("Member not found")



    def update_member(self, request, group_id, member_id):
        """
        User with access can update member role

        Parameters:
            request (request): request data
            group_id (uuid): group id
            member_id (uuid): member id
        
        Returns:
            dict: member data
        """
        print("request data : \n\n\n\n", request.data)
        try:
            role_id = request.data['role']
        except Exception as e:
            raise Exception("Please select new role to assign" + str(e))
        
        member = GroupMember.objects.get(id=member_id)
        if str(member.group.id) != group_id:
            raise Exception("Member not found")
        role = RolePermission.objects.get(id=role_id)
        member.role = role
        member.save(username = member.user.username, email_id = member.user.email)
        ser = MemberSerializer(member)
        return {'data':ser.data, 'errors':None}

    def delete_member(self, request, group_id, member_id):
        """
        User with access can remove member from group

        Parameters:
            request (request): request data
            group_id (uuid): group id
            member_id (uuid): member id
        
        Returns:
            dict: member data
        """
        obj = GroupMember.objects.get(id=member_id)
        if obj.group.id == group_id:
            obj.delete()
            return {'data':None, 'errors':None}
        raise Exception("Member not found")
    
    def invite_member(self, request, group_id):  
        """
        users in group with access can invite users to join group
        """
        try:
            user_id = request.data['user']
        except:
            raise Exception("Please select user to invite")
        try:
            role_id = request.data['role']
        except Exception as e:
            raise Exception("Please select role for member")
        
        user = CustomUser.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        role = RolePermission.objects.get(id=role_id)
        member = GroupMember.objects.create(group=group, user=user, is_invited=True, role = role)
        member.save(email_id = user.email, username = user.username)
        ser = MemberSerializer(member)
        return {'data':ser.data, 'errors':None}

    def accept_member(self, request, member_id):
        """
        User can accept invitation to join group

        Parameters:
            request (request): request data
            member_id (uuid): member id

        Returns:
            Void
        """
        member = GroupMember.objects.get(id=member_id)
        member.is_pending = False
        member.save()

    def join_as_member(self, request, group_id):
        """
        User can join group as member.

        Parameters:
            request (request): request data
            group_id (uuid): group id

        Returns:
            dict: member data
        """
        print("joining")
        group = Group.objects.get(id=group_id)
        user = request.user
        print("got user")
        perm = RolePermission.objects.filter(group = group)
        perm = perm.get(is_default=True)
        is_invited = group.is_public_join
        print("generating member")
        member = GroupMember.objects.create(group=group, user=user, is_invited=is_invited, role = perm, username = user.username, email_id = user.email)
        print("obj created")
        member.username = user.username
        member.email_id = user.email
        member.save()
        ser = MemberSerializer(member)
        return {'data':ser.data, 'errors':None}
    
    def get_my_member(self, request, group_id):
        """
        User can get his member details

        Parameters:
            request (request): request data
            group_id (uuid): group id

        Returns:
            dict: member data
        """
        group = Group.objects.get(id=group_id)
        user = request.user
        member = GroupMember.objects.filter(group=group).get(user=user)
        ser = MemberSerializer(member)
        return {'data':ser.data, 'errors':None}