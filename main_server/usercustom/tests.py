from django.test import TestCase,Client
from .views import *
from .models import *
from usercustom.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from otpdetails.models import Otpdetails

class Tests(TestCase):
    databases = ['default', 'groups_ind']
    def setUp(self):
        self.c_user = CustomUser.objects.create(email = "1125@gmail.com",username='testuser5', password = 'testpassword', first_name='test', last_name='user', is_activated=True)
        self.c_user.save()
        self.c_user.set_password('testpassword')
        self.c_user.save()
        self.c_user_1 = CustomUser.objects.create(email = "1126@gmail.com",username='testuser6', password = 'testpassword2', first_name='test2', last_name='user2', is_activated=True)
        self.c_user_1.save()

    def test_register(self):
        data={
            "email": "2020csb11111@gmail.com",
            "username": "testuser1223",
            "password": "testpassword",
            "first_name": "test",
            "last_name": "user",
        }
        response = self.client.post('/user/register/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        data={
            "email": self.c_user.email,
            "password":'testpassword',
        }
        response = self.client.post('/user/login/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data={
            "email": self.c_user.email,
            "password":'testpasswor',
        }
        response = self.client.post('/user/login/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data={
            "email": "hello@hai.com",
            "password":'testpasswor',
        }
        response = self.client.post('/user/login/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_user(self):
        response = self.client.get(f'/user/getuser/{self.c_user.id}/')
        self.assertEqual(response.data['email'], self.c_user.email)
        self.assertEqual(response.status_code, 200)
    
    def test_login_otp(self):
        data = {
            "email": self.c_user.email,
        }
        response = self.client.post('/user/login_otp/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_verify_otp(self):
        otp = Otpdetails.objects.create(user = self.c_user)
        otp.setup()
        print("user otp: ",otp.otp)
        otp.save()
        data = {
            "email": self.c_user.email,
            "otp": otp.otp,
        }
        response = self.client.put('/user/login_otp/', data= data, content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        data = {
            "email": self.c_user.email,
            "otp": '243244',
        }
        response = self.client.put('/user/login_otp/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    def test_profile(self):
        accessTo = str(RefreshToken.for_user(self.c_user).access_token)
        new_cli =  Client()
        new_cli.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + accessTo
        response = new_cli.get('/user/profile/')
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        accessTo = str(RefreshToken.for_user(self.c_user).access_token)
        new_cli =  Client()
        new_cli.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + accessTo
        data = {
            "first_name": "test",
            "last_name": "user",
        }
        response = new_cli.put('/user/profile/', data= data, content_type='application/json')
        self.assertEqual(response.status_code, 200)



        
