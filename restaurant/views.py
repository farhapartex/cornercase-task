from django.utils import timezone
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters
from user.permissions import IsAdminOrOwner, IsOwner, IsEmployee
from restaurant.serializers import RestaurantCreateSerializer, MenuCreateSerializer, MenuListSerializer
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
    queryset = Menu.objects.all()
    serializer_class = MenuListSerializer
    permission_classes = (IsAuthenticated, IsEmployee)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MenuFilter

    def get_queryset(self):
        today = timezone.now().date()
        return Menu.objects.filter(created_at__date=today)

