from django.test import TestCase,Client
from .views import *
from .models import *
from usercustom.models import CustomUser
from permissions.models import RolePermission
from member.models import GroupMember
from rest_framework_simplejwt.tokens import RefreshToken
# Create your tests here.
# Tests for permissions

class Tests(TestCase):

    def setUp(self):
        self.c_user = CustomUser.objects.create(email = "1121@gmail.com",username='testuser', password = 'testpassword', first_name='test', last_name='user', is_activated=True)
        self.c_user.save()
        self.c_user_1 = CustomUser.objects.create(email = "111@gmail.com",username='testuser2', password = 'testpassword2', first_name='test2', last_name='user2', is_activated=True)
        self.c_user_1.save()
        self.group = Group.objects.create(name='testgroup', description='test description', created_by=self.c_user, db_region='groups_ind')
        self.group.save()
        self.member = RolePermission.objects.create(role_name='member', role_description='test description', group=self.group , is_default=True)
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
        self.request = self.client.post(f'/thread/group/{self.group.id}/', content_type='application/json', data = {'message':'test message', 'subject':'test subject'})
        print('response_data\n\n\n\n\n\n', self.request.data.get('data')['id'], self.request.status_code)
        self.thread = MessageThread.objects.get(id = self.request.data.get('data')['id'])
        
    
    def test_tread(self):
        self.assertEqual(self.request.status_code, 200)
    
    def test_permission_can_view_thread(self):
        self.assertEqual(can_view_thread(self.c_user, self.thread.id), True)
        self.assertEqual(can_view_thread(self.c_user_1, self.thread.id), False)
        self.assertEqual(can_view_thread(self.c_user_1, 'self.thread.id'), False)
    
    def test_can_view_grp_messages(self):
        self.assertEqual(can_view_grp_messages(self.c_user, self.group.id), True)
        self.assertEqual(can_view_grp_messages(self.c_user_1, self.group.id), False)
        self.assertEqual(can_view_grp_messages(self.c_user_1, 'self.group.id'), False)
    
    def test_view_thread(self):
        self.assertEqual(self.client.get(f'/thread/{self.thread.id}/').status_code, 200)
        self.assertEqual(self.client2.get(f'/thread/{self.thread.id}/').status_code, 401)
    
    def test_view_threads(self):
        self.assertEqual(self.client.get(f'/thread/group/{self.group.id}/').status_code, 200)
        self.assertEqual(self.client2.get(f'/thread/group/{self.group.id}/').status_code, 401)
    
    def test_create_user(self):
        user1 = CustomUser.objects.create_user(email = "2020csb1121@iitrpr.ac.in", password = "Sour@1234")
        user1.save()
        user2 = CustomUser.objects.create_superuser(email="2020csb11222@iitrpr.ac.in", password = "Sour@1234")
        user2.save()
        user3 = CustomUser.objectsall.create_user(email = "2020csb1123@iitrpr.ac.in", password = "Sour@1234")
        user3.save()
        user4 = CustomUser.objectsall.create_superuser(email = "2020csb1124@iitrpr.ac.in", password = "Sour@1234")
        user4.save()
        self.assertEqual(user1.email, "2020csb1121@iitrpr.ac.in")
        self.assertEqual(user2.email, "2020csb11222@iitrpr.ac.in")
        self.assertEqual(user3.email, "2020csb1123@iitrpr.ac.in")
        self.assertEqual(user4.email, "2020csb1124@iitrpr.ac.in")