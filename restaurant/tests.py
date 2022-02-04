from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from user.enums import RoleChoices


class RestaurantCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_admin = User.objects.create(username="dev1@test.com", email="dev1@test.com",
                                              role=RoleChoices.ADMIN.value)
        self.user_admin.set_password("Test123")

        self.user_employee = User.objects.create(username="dev2@test.com", email="dev2@test.com",
                                                 role=RoleChoices.EMPLOYEE.value)
        self.user_employee.set_password("Test123")

        self.user_owner = User.objects.create(username="dev3@test.com", email="dev3@test.com",
                                              role=RoleChoices.OWNER.value)
        self.user_owner.set_password("Test123")

    def test_api_get_method(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(reverse("create-restaurant"), format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_restaurant_creation_by_admin(self):
        """
        1. If Admin want to create a restaurant, he/she have to pass owner information (owner_email)
        2. Admin can't set himself as a owner
        :return:
        """
        self.client.force_authenticate(user=self.user_admin)

        request_data = {
            "name": "Test"
        }
        response = self.client.post(reverse("create-restaurant"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_data = {
            "name": "Test",
            "owner_email": self.user_admin.email
        }
        response = self.client.post(reverse("create-restaurant"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_data = {
            "name": "Test",
            "owner_email": self.user_owner.email
        }
        response = self.client.post(reverse("create-restaurant"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurant_creation_by_owner(self):
        """
        1. If Owner want to create a restaurant, he/she don't need to pass owner information (owner_email)
        2. A Owner can't create restaurant for another owner
        :return:
        """
        self.client.force_authenticate(user=self.user_owner)

        request_data = {
            "name": "Test"
        }
        response = self.client.post(reverse("create-restaurant"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request_data = {
            "name": "Test 2",
            "owner_email": self.user_owner.email
        }
        response = self.client.post(reverse("create-restaurant"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_owner2 = User.objects.create(username="dev4@test.com", email="dev4@test.com", role=RoleChoices.OWNER.value)
        request_data = {
            "name": "Test 2",
            "owner_email": user_owner2.email
        }
        response = self.client.post(reverse("create-restaurant"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
