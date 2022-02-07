from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from user.models import User
from user.enums import RoleChoices
from restaurant.models import Restaurant
from vote.models import Vote


class VoteCreateSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()

    def validate(self, attrs):
        request_user = self.context["request"].user
        if request_user.role != RoleChoices.EMPLOYEE.value:
            raise serializers.ValidationError(detail="User is not employee")
        attrs["employee"] = request_user

        restaurant = Restaurant.get_restaurant_instance(id=attrs["restaurant_id"])

        if restaurant is None:
            raise serializers.ValidationError(detail="Restaurant not found")
        attrs["restaurant"] = restaurant

        # check if there are menus for today for the restaurant
        today = timezone.now().date()
        menus = restaurant.menus.filter(created_at__date=today)
        if menus.count() == 0:
            raise serializers.ValidationError(detail="Menu not found for the restaurant")

        if Vote.is_has_employee_vote(employee=request_user):
            raise serializers.ValidationError(detail="Employee already set vote for today")

        return attrs

    def create(self, validated_data):
        request_data = {
            "employee": validated_data["employee"],
            "restaurant": validated_data["restaurant"]
        }

        with transaction.atomic():
            instance = Vote.objects.create(**request_data)

            return instance


