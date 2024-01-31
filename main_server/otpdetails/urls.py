from django.urls import path
from .views import *
app_name = 'validation'

urlpatterns = [
    path('verify/<str:email>/<str:slug>/', Verify.as_view(), name='verify'),
    path('invalidate/<str:email>/<str:slug>/', Invalidate.as_view(), name='invalidate'),
]
