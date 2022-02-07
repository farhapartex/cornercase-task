import logging
from django.db import transaction
from rest_framework import serializers
from user.models import User
from user.enums import RoleChoices

logger = logging.getLogger("django")


class UserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.CharField()

    def create(self, validated_data):
        if validated_data["role"] not in RoleChoices.get_all():
            raise serializers.ValidationError("User role is not found")

        request_data = {
            "first_name": validated_data.get("first_name", ""),
            "last_name": validated_data.get("last_name", ""),
            "email": validated_data.get("email"),
            "username": validated_data.get("email"),
            "role": validated_data.get("role"),
            "is_active": True
        }

        with transaction.atomic():
            user = User.objects.create(**request_data)
            user.set_password(validated_data.get("password"))
            user.save()
            logger.info(f"{user.username} created successfully")

            return user