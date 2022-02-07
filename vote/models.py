from django.db import models
from django.utils import timezone
from core.base_model import BaseAbstractModel
from restaurant.models import Restaurant
from user.models import User
# Create your models here.


class Vote(BaseAbstractModel):
    restaurant = models.ForeignKey(Restaurant, related_name="votes", on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(User, related_name="employee_votes", on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id)

    @classmethod
    def is_has_employee_vote(cls, *, employee: User):
        vote = Vote.objects.filter(employee=employee, created_at__date=timezone.now().date()).first()
        return True if vote else False

    @classmethod
    def get_vote_instance_by_restaurant(cls, restaurant_id):
        vote = Vote.objects.filter(restaurant_id=restaurant_id).first()
        return vote



class VoteResult(BaseAbstractModel):
    restaurant = models.ForeignKey(Restaurant, related_name="wins", on_delete=models.DO_NOTHING)
    votes = models.IntegerField()

    def __str__(self):
        return f"{self.restaurant}-{self.votes}"
