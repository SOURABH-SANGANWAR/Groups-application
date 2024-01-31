from django.test import TestCase,Client
from .views import *
from .models import *
from .permissions import *
from usercustom.models import CustomUser
from permissions.models import RolePermission
from member.models import GroupMember
from rest_framework_simplejwt.tokens import RefreshToken
# Create your tests here.
# Tests for permissions

class Tests(TestCase):
    databases = ['default', 'groups_ind']

    def setUp(self):
        self.c_user = CustomUser.objects.create(email = "1125@gmail.com",username='testuser', password = 'testpassword', first_name='test', last_name='user', is_activated=True)
        self.c_user.save()
        self.c_user_1 = CustomUser.objects.create(email = "116@gmail.com",username='testuser2', password = 'testpassword2', first_name='test2', last_name='user2', is_activated=True)
        self.c_user_1.save()
        self.group = Group.objects.create(name='testgroup', description='test description', created_by=self.c_user, db_region='groups_ind',   is_public_view = True, is_public_join = True)
        self.group.save()
        self.member = RolePermission.objects.create(role_name='member', role_description='test description', group=self.group, is_default = True)
        self.member.save()
        self.admin = RolePermission.objects.create(role_name='admin', role_description='test description', group=self.group,manage_members=True,  manage_metadata = True, manage_content = True, manage_roles = True)
        self.admin.save()
        self.group_member = GroupMember.objects.create(user=self.c_user, group=self.group, role=self.admin)
        self.group_member.save()
        self.token = RefreshToken.for_user(self.c_user)
        self.access_token = str(self.token.access_token)
        self.client = Client()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.access_token}'
        self.client2 = Client()
        self.token2 = RefreshToken.for_user(self.c_user_1)
        self.access_token2 = str(self.token2.access_token)
        self.client2.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.access_token2}'
    
    def test_is_user_member_manager(self):
        self.assertTrue(is_user_member_manager(self.c_user.id, self.group.id))
        self.assertFalse(is_user_member_manager(self.c_user_1.id, self.group.id))
    
    def test_group_members_view(self):
        response = self.client.get(f'/member/group/{self.group.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.client2.get(f'/member/group/{self.group.id}/')
        self.assertEqual(response.status_code, 401)
    
    def test_group_members_create(self):
        response = self.client.post(f'/member/group/{self.group.id}/', {'user':self.c_user_1.id, 'group':self.group.id, 'role':self.member.id}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post(f'/member/group/{self.group.id}/', {'user':self.c_user_1.id, 'group':self.group.id, 'role':self.member.id}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
    
    def test_group_member_get(self):
        response = self.client.get(f'/member/group/get/{self.group.id}/{self.group_member.id}/')

        self.assertEqual(response.status_code, 200)
    
    def test_group_ember_put(self):

        response = self.client.put(f'/member/group/get/{self.group.id}/{self.group_member.id}/', {'role':self.admin.id}, content_type='application/json')

        self.assertEqual(response.status_code, 200)
    
    def test_group_delete(self):
        response = self.client.delete(f'/member/group/get/{self.group.id}/nan/')
        self.assertEqual(response.status_code, 400)
    
    def test_accept_request(self):
        response = self.client.put(f'/member/group/{self.group.id}/{self.group_member.id}/accept/')
        self.assertEqual(response.status_code, 200)
        response = self.client2.put(f'/member/group/{self.group.id}/abcdefgh/accept/')
        self.assertEqual(response.status_code, 401)
    
    def test_join(self):
        response = self.client2.put(f'/member/group/{self.group.id}/join/')
        self.assertEqual(response.status_code, 200)
        response = self.client2.put(f'/member/group/{self.group.id}/join/')
        self.assertEqual(response.status_code, 400)

