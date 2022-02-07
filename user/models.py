from django.db import models
from django.contrib.auth.models import AbstractUser
from core.base_model import BaseAbstractModel
from user.enums import RoleChoices


class User(BaseAbstractModel, AbstractUser):
    role = models.CharField(max_length=120, choices=RoleChoices.choices, default=RoleChoices.ADMIN.value)

    @classmethod
    def get_user_instance(cls, *, username=None, id=None):
        if username:
            return cls.objects.filter(username=username).first()
        return cls.objects.filter(id=id).first()

    def __str__(self):
        return self.username

