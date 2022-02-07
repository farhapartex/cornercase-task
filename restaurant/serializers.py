import logging
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from restaurant.models import Restaurant, Menu
from user.enums import RoleChoices
from user.models import User

logger = logging.getLogger(__name__)


class RestaurantCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    owner_email = serializers.EmailField(required=False)

    def create(self, validated_data):
        user = self.context["request"].user
        owner = None
        if "owner_email" in validated_data:
            owner = get_object_or_404(User, email=validated_data["owner_email"])
            if owner.role != RoleChoices.OWNER.value:
                raise serializers.ValidationError(detail="User is not a owner")

        if user.role == RoleChoices.OWNER.value:
            if owner and owner.email != user.email:
                raise serializers.ValidationError(detail="Owner can't create restaurant for another owner")
            else:
                owner = user
        elif user.role == RoleChoices.ADMIN.value:
            if owner is None:
                raise serializers.ValidationError(detail="Restaurant owner email is missing")
            elif owner.email == user.email:
                raise serializers.ValidationError(detail="Admin can't assign him as a owner")

        request_body = {
            "name": validated_data.get("name"),
            "owner": owner
        }

        with transaction.atomic():
            instance = Restaurant.objects.create(**request_body)
            logger.info(f"Restaurant {instance.name} {instance.id} created")
            return instance


class MenuCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    restaurant_id = serializers.IntegerField()
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    def validate(self, attrs):
        user = self.context["request"].user
        restaurant = Restaurant.objects.filter(id=attrs["restaurant_id"]).select_related('owner').first()
        if restaurant is None:
            raise serializers.ValidationError(detail="Restaurant not found")
        if restaurant.owner.username != user.username:
            raise serializers.ValidationError(detail="Restaurant owner mismatch")

        attrs["restaurant"] = restaurant
        return attrs

    def create(self, validated_data):
        request_data = {
            "name": validated_data["name"],
            "restaurant": validated_data["restaurant"],
            "description": validated_data.get("description", ""),
            "price": validated_data["price"],
        }

        with transaction.atomic():
            instance = Menu.objects.create(**request_data)
            logger.info(f"Menu {instance.name} {instance.id} created for Restaurant: {instance.restaurant.name}")

            return instance


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("id", "name", "price")


class RestaurantMenuListSerializer(serializers.ModelSerializer):
    menus = serializers.SerializerMethodField()

    def get_menus(self, instance):
        queryset = instance.menus.filter(created_at__date=timezone.now().date())
        return MenuSerializer(queryset, many=True).data

    class Meta:
        model = Restaurant
        fields = ("id", "name", "menus",)
