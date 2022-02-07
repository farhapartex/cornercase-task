from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vote.models import Vote
from vote.serializers import VoteCreateSerializer
from user.permissions import IsEmployee
# Create your views here.


class VoteCreateAPIView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    permission_classes = (IsAuthenticated, IsEmployee)
    serializer_class = VoteCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"status": "Success"}, status=status.HTTP_201_CREATED)

