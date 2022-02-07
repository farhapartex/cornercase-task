from django.utils import timezone
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters
from user.permissions import IsAdminOrOwner, IsOwner, IsEmployee
from restaurant.serializers import RestaurantCreateSerializer, MenuCreateSerializer, RestaurantMenuListSerializer
from restaurant.models import Restaurant, Menu
from restaurant.filters import MenuFilter
# Create your views here.


class RestaurantCreateAPIView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrOwner)
    serializer_class = RestaurantCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"status": "Success"}, status=status.HTTP_201_CREATED)


class MenuCreateAPIView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = MenuCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"status": "Success"}, status=status.HTTP_201_CREATED)


class MenuListAPIView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantMenuListSerializer
    permission_classes = (IsAuthenticated, IsEmployee)

