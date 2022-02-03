from django.urls import re_path, include
from user.views import UserCreateAPIView

urlpatterns = [
    re_path(r'^api/v1/create-user/$', UserCreateAPIView.as_view(), name='create-user'),
]
