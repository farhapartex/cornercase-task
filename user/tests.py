from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from user.enums import RoleChoices


class UserCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_admin = User.objects.create(username="dev1", role=RoleChoices.ADMIN.value)
        self.user_admin.set_password("Test123")

        self.user_employee = User.objects.create(username="dev2", role=RoleChoices.EMPLOYEE.value)
        self.user_employee.set_password("Test123")

        self.user_owner = User.objects.create(username="dev3", role=RoleChoices.OWNER.value)
        self.user_owner.set_password("Test123")

    def test_api_get_method(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(reverse("create-user"), format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_employee_validation_by_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        request_body = {
            "email": "employee1@test.com",
            "role": "employe",
            "password": "Test123"
        }

        response = self.client.post(reverse("create-user"), data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body = {
            "email": "employee1@test.com",
            "password": "Test123"
        }

        response = self.client.post(reverse("create-user"), data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_employee_by_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        request_body = {
            "email": "employee1@test.com",
            "role": "employee",
            "password": "Test123"
        }

        response = self.client.post(reverse("create-user"), data=request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="employee1@test.com")
        self.assertEqual(user.username, user.email)
        self.assertEqual(user.role, RoleChoices.EMPLOYEE.value)

    def test_create_any_user_by_employee(self):
        self.client.force_authenticate(user=self.user_employee)
        request_body = {
            "email": "employee1@test.com",
            "role": "employee",
            "password": "Test123"
        }

        response = self.client.post(reverse("create-user"), data=request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request_body = {
            "email": "employee1@test.com",
            "role": "owner",
            "password": "Test123"
        }

        response = self.client.post(reverse("create-user"), data=request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_any_user_by_owner(self):
        self.client.force_authenticate(user=self.user_employee)
        request_body = {
            "email": "employee1@test.com",
            "role": "employee",
            "password": "Test123"
        }

        response = self.client.post(reverse("create-user"), data=request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request_body = {
            "email": "employee1@test.com",
            "role": "owner",
            "password": "Test123"
        }

        response = self.client.post(reverse("create-user"), data=request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)