from django.urls import re_path
from vote.views import VoteCreateAPIView

urlpatterns = [
    re_path(r'^api/v1/create-vote/$', VoteCreateAPIView.as_view(), name='create-vote'),
]
