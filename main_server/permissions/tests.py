from django.test import TestCase,Client
from .views import *
from .models import *
from .permissions import *
from usercustom.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
# Create your tests here.
# Tests for permissions

class Tests(TestCase):
    databases = ['default', 'groups_ind']

    def setUp(self):
        self.c_user = CustomUser.objects.create(email = "1122@gmail.com",username='testuser3', password = 'testpassword', first_name='test', last_name='user', is_activated=True)
        self.c_user.save()
        self.c_user_1 = CustomUser.objects.create(email = "1123@gmail.com",username='testuser4', password = 'testpassword2', first_name='test2', last_name='user2', is_activated=True)
        self.c_user_1.save()
        self.group = Group.objects.create(name='testgroup', description='test description', created_by=self.c_user, db_region='groups_ind')
        self.group.save()
        self.member = RolePermission.objects.create(role_name='member', role_description='test description', group=self.group)
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

    def test_can_manage_roles(self):
        self.assertTrue(can_manage_roles(self.c_user.id, self.group.id))
        self.assertFalse(can_manage_roles(self.c_user.id, "hello"))
    
    def test_role_permission_list(self):
        request = self.client.get(f'/role/group/{self.group.id}/')
        self.assertEqual(request.status_code, 200)
        request = self.client2.get(f'/role/group/{self.group.id}/')
        self.assertEqual(request.status_code, 401)
    
    def test_role_permission_create(self):
        request = self.client.post(f'/role/group/{self.group.id}/', {'role_name':'testrole', 'role_description':'test description', 'is_default':False, 'manage_members':True, 'manage_metadata':True, 'manage_content':True, 'manage_roles':True})
        self.assertEqual(request.status_code, 201)
        request = self.client2.post(f'/role/group/{self.group.id}/', {'role_name':'testrole', 'role_description':'test description', 'is_default':True, 'manage_members':True, 'manage_metadata':True, 'manage_content':True, 'manage_roles':True})
        self.assertEqual(request.status_code, 401)
        request = self.client.post(f'/role/group/{self.group.id}/', {'role_name':'testrole', 'role_description':'test description', 'is_default':True, 'manage_members':True, 'manage_metadata':True, 'manage_content':True, 'manage_roles':True})
        self.assertEqual(request.status_code, 400)
    
    def test_get_detail_view(self):
        request = self.client.get(f'/role/group/{self.group.id}/{self.admin.id}/')
        self.assertEqual(request.status_code, 200)
        request = self.client2.get(f'/role/group/{self.group.id}/{self.admin.id}/')
        self.assertEqual(request.status_code, 401)
    
    def test_put_detail_view(self):
        request = self.client.put(f'/role/group/{self.group.id}/{self.admin.id}/', data = {'role_name':'admin','role_description':"admin",'manage_roles':True}, content_type='application/json')
        print("putdata:\n\n\n\n",request.data)
        self.assertEqual(request.status_code, 200)
        request = self.client2.put(f'/role/group/{self.group.id}/{self.member.id}/', data = {'manage_roles':False}, content_type='application/json')
        self.assertEqual(request.status_code, 401)
    
    def test_delete_detail_view(self):
        request = self.client.delete(f'/role/group/{self.group.id}/{self.admin.id}/')
        self.assertEqual(request.status_code, 200)
        request = self.client2.delete(f'/role/group/{self.group.id}/{self.member.id}/')
        self.assertEqual(request.status_code, 401)
