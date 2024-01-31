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
        self.c_user = CustomUser.objects.create(email = "1121@gmail.com",username='testuser', password = 'testpassword', first_name='test', last_name='user', is_activated=True)
        self.c_user.save()
        self.c_user_1 = CustomUser.objects.create(email = "111@gmail.com",username='testuser2', password = 'testpassword2', first_name='test2', last_name='user2', is_activated=True)
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


    def test_is_group_admin(self):
        self.assertTrue(is_group_admin(self.c_user.id, self.group.id))
        self.assertFalse(is_group_admin(self.c_user.id, "hello"))     

    def test_can_view_group(self):
        self.assertTrue(can_view_group(self.c_user.id, self.group))
        self.assertFalse(can_view_group(self.c_user.id, "hello"))
    
    def test_create_client_group(self):
        data={
            "name": "testgroup1",
            "description": "test description",
            "db_region": "groups_ind",
            "email":"temp@gmail.com",
            "password":"temp1234"
        }
        response = self.client.post('/group/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data={
            "name": "testgroup",
            "description": "test description",
        }
        response = self.client.post('/group/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_group(self):
        response = self.client.get('/group/get/'+str(self.group.id)+'/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/group/get/'+"hello"+'/')
        self.assertEqual(response.status_code, 400)
        response = self.client2.get('/group/get/'+str(self.group.id)+'/')
        self.assertEqual(response.status_code, 401)

    def test_get_group_list(self):
        response = self.client.get('/group/user/')
        self.assertEqual(response.status_code, 200)
    
    def test_edit_group(self):
        data={
            "name": "testgroup",
            "description": "test descript"
        }
        response = self.client.put('/group/get/'+str(self.group.id)+'/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client2.put('/group/get/'+str(self.group.id)+'/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    
    def test_delete_group(self):
        response = self.client.delete('/group/get/'+str(self.group.id)+'/')
        self.assertEqual(response.status_code, 200)
        response = self.client.delete('/group/get/'+str(self.group.id)+'/')
        self.assertEqual(response.status_code, 400)
        response = self.client2.delete('/group/get/'+str(self.group.id)+'/')
        self.assertEqual(response.status_code, 401)
    


        


# class TestSerializers(TestCase):
#     databases = ['default', 'groups_ind']

#     def 