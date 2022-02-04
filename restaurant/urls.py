from django.urls import re_path, include
from restaurant.views import RestaurantCreateAPIView

urlpatterns = [
    re_path(r'^api/v1/create-restaurant/$', RestaurantCreateAPIView.as_view(), name='create-restaurant'),
]