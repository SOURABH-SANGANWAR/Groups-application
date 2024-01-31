from .views import *
from django.urls import path

app_name = 'member'

urlpatterns = [
    path('group/<slug:group_id>/', GroupMemberView.as_view()),
    path('group/get/<slug:group_id>/<slug:member_id>/', GetGroupMember.as_view()),
    path('group/<slug:group_id>/<slug:member_id>/accept/', AcceptMember.as_view()),
    path('group/<slug:group_id>/join/', JoinAsMember.as_view()),
]