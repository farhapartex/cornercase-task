from django.db import models
from django.contrib.auth.models import AbstractUser
from core.base_model import BaseAbstractModel
from user.enums import RoleChoices


class User(BaseAbstractModel, AbstractUser):
    role = models.CharField(max_length=120, choices=RoleChoices.choices, default=RoleChoices.ADMIN.value)

    def __str__(self):
        return str(self.id)


