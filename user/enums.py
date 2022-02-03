from django.db import models


class RoleChoices(models.TextChoices):
    ADMIN = "admin", "Admin"
    OWNER = "owner", "Owner"
    EMPLOYEE = "employee", "Employee"

