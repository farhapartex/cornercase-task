from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from user.models import User
from user.serializers import UserCreateSerializer
from user.permissions import IsAdmin, IsEmployee
# Create your views here.


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
