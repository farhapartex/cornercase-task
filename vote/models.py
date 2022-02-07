from django.db import models
from core.base_model import BaseAbstractModel
from restaurant.models import Restaurant
from user.models import User
# Create your models here.


class Vote(BaseAbstractModel):
    restaurant = models.ForeignKey(Restaurant, related_name="votes", on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(User, related_name="employee_votes", on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id)


