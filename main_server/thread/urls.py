from django.urls import path
from .views import *

app_name = 'thread'

urlpatterns = [
    path('<slug:id>/', ThreadDetailView.as_view()),
    path('group/<slug:group_id>/', ThreadView.as_view()),
]