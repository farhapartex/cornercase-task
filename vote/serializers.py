from django.db import transaction
from django.utils import timezone
from django.db.models import Count
from rest_framework import serializers
from user.enums import RoleChoices
from restaurant.models import Restaurant
from vote.models import Vote, VoteResult


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

            vote_result = VoteResult.objects.filter(created_at__date=timezone.now().date()).first()
            if vote_result is None:
                VoteResult.objects.create(restaurant=instance.restaurant, votes=1)
            else:
                votes = Vote.objects.filter(created_at__date=timezone.now().date()).values_list('restaurant').annotate(res_count=Count('restaurant')).order_by(
                    '-res_count')
                all_votes = VoteResult.objects.all().order_by("-id")

                restaurant = Restaurant.get_restaurant_instance(id=votes[0][0])
                if all_votes.count() >= 3:
                    if all_votes[0].restaurent.id == restaurant.id and all_votes[1].restaurent.id == restaurant.id and all_votes[2].restaurent.id == restaurant.id:
                        if len(votes) > 1:
                            restaurant = Restaurant.get_restaurant_instance(id=votes[1][0])

                vote_result.restaurant = restaurant
                vote_result.votes = votes[0][1]
                vote_result.save()

            return instance


class VoteResultSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    result_date = serializers.SerializerMethodField()

    def get_restaurant(self, instance):
        return {
            "id": instance.restaurant.id,
            "name": instance.restaurant.name
        }

    def get_result_date(self, instance):
        return str(instance.created_at.date())

    class Meta:
        model = VoteResult
        fields = ("id", "restaurant", "votes", "result_date")
