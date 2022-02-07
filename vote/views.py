from django.utils import timezone
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vote.models import Vote, VoteResult
from vote.serializers import VoteCreateSerializer, VoteResultSerializer
from user.permissions import IsEmployee
# Create your views here.


class VoteCreateAPIView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    permission_classes = (IsAuthenticated, IsEmployee)
    serializer_class = VoteCreateSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"status": "Success"}, status=status.HTTP_201_CREATED)


class VoteResultAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        vote_result = VoteResult.objects.filter(created_at__date=timezone.now().date()).first()
        if vote_result is None:
            return Response(data={"message": "Vote not found for today"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VoteResultSerializer(vote_result)

        return Response(data=serializer.data)

