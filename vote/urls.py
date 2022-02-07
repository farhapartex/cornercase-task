from django.urls import re_path
from vote.views import VoteCreateAPIView, VoteResultAPIView

urlpatterns = [
    re_path(r'^api/v1/create-vote/$', VoteCreateAPIView.as_view(), name='create-vote'),
    re_path(r'^api/v1/vote-result/$', VoteResultAPIView.as_view(), name='vote-result'),
]
