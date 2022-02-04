from django.db import models
from core.base_model import BaseAbstractModel
from user.models import User
# Create your models here.


class Restaurant(BaseAbstractModel):
    owner = models.ForeignKey(User, related_name="restaurants", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Menu(BaseAbstractModel):
    restaurant = models.ForeignKey(Restaurant, related_name="menus", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.id)
