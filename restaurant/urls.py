from django.urls import re_path, include
from restaurant.views import RestaurantCreateAPIView, MenuCreateAPIView

urlpatterns = [
    re_path(r'^api/v1/create-restaurant/$', RestaurantCreateAPIView.as_view(), name='create-restaurant'),
    re_path(r'^api/v1/create-menu/$', MenuCreateAPIView.as_view(), name='create-menu'),
]