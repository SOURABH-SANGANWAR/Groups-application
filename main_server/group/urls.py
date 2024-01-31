from django.urls import path
from .views import *
app_name = 'group'

urlpatterns = [
    path('', GroupsView.as_view(), name='groups'),
    path('get/<slug:id>/', GroupView.as_view(), name='group'),
    path('user/', GroupsUserView.as_view(), name='user_groups'),
]