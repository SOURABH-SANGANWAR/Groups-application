from .views import *
from django.urls import path

app_name = 'role'

urlpatterns = [
    path('group/<slug:group_id>/', RolePermissionView.as_view()),
    path('group/<slug:group_id>/<slug:id>/', RolePermissionDetailView.as_view()),
]
