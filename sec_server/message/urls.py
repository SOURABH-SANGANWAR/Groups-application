from .views import *
from django.urls import path
app_name = 'message'

urlpatterns = [
    path('<slug:id>/', messageView.as_view()),
    path('attachment/<slug:id>/<int:attach_id>/', GetAttachment.as_view()),
]   