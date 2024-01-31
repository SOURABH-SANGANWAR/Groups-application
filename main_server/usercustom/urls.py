from django.urls import path
from .views import *
app_name = 'usercustom'

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('getuser/<slug:id>/', getUser.as_view(), name='getuser'),
    path('login/', Login.as_view(), name = 'login'),
    path('login_otp/', LoginOtp.as_view(), name = 'login_otp'),
    path('profile/', Profile.as_view(), name = 'profile'),
]