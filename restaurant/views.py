from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.permissions import IsAdminOrOwner
from restaurant.serializers import RestaurantCreateSerializer
from restaurant.models import Restaurant, Menu
# Create your views here.


class RestaurantCreateAPIView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrOwner)
    serializer_class = RestaurantCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
