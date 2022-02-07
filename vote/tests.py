from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from vote.models import Vote
from restaurant.models import Restaurant, Menu
from user.models import User
from user.enums import RoleChoices
# Create your tests here.


class VoteCreateAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user_admin = User.objects.create(username="dev1@gmail.com", email="dev1@gmail.com", role=RoleChoices.ADMIN.value)
        self.user_admin.set_password("Test123")

        self.user_employee = User.objects.create(username="dev2@gmail.com", email="dev2@gmail.com",  role=RoleChoices.EMPLOYEE.value)
        self.user_employee.set_password("Test123")

        self.user_owner1 = User.objects.create(username="dev3@gmail.com", email="dev3@gmail.com",  role=RoleChoices.OWNER.value)
        self.user_owner1.set_password("Test123")

        self.user_owner1 = User.objects.create(username="dev4@gmail.com", email="dev4@gmail.com",  role=RoleChoices.OWNER.value)
        self.user_owner1.set_password("Test123")

        self.user_owner2 = User.objects.create(username="dev5@gmail.com", email="dev5@gmail.com",
                                               role=RoleChoices.OWNER.value)
        self.user_owner2.set_password("Test123")

    def test_api_get_method(self):
        self.client.force_authenticate(user=self.user_employee)
        response = self.client.get(reverse("create-vote"), format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_access_by_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(reverse("create-vote"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_access_by_owner(self):
        self.client.force_authenticate(user=self.user_owner1)
        response = self.client.get(reverse("create-vote"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_validation(self):
        self.client.force_authenticate(user=self.user_employee)
        request_data = {
            "restaurant_id": 100
        }
        response = self.client.post(reverse("create-vote"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Restaurant has no menu
        restaurant1 = Restaurant.objects.create(owner=self.user_owner1, name="Test Restaurant 1")
        request_data = {
            "restaurant_id": restaurant1.id
        }
        response = self.client.post(reverse("create-vote"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_by_employee(self):
        self.client.force_authenticate(user=self.user_employee)
        restaurant1 = Restaurant.objects.create(owner=self.user_owner1, name="Test Restaurant 1")
        restaurant2 = Restaurant.objects.create(owner=self.user_owner2, name="Test Restaurant 2")

        Menu.objects.create(name="Test menu 1", restaurant=restaurant1, price=100.00)
        Menu.objects.create(name="Test menu 2", restaurant=restaurant1, price=200.00)
        Menu.objects.create(name="Test menu 3", restaurant=restaurant2, price=200.00)

        request_data = {
            "restaurant_id": restaurant1.id
        }

        response = self.client.post(reverse("create-vote"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_single_voting_by_employee(self):
        self.client.force_authenticate(user=self.user_employee)

        restaurant1 = Restaurant.objects.create(owner=self.user_owner1, name="Test Restaurant 1")
        restaurant2 = Restaurant.objects.create(owner=self.user_owner2, name="Test Restaurant 2")

        Menu.objects.create(name="Test menu 1", restaurant=restaurant1, price=100.00)
        Menu.objects.create(name="Test menu 2", restaurant=restaurant1, price=200.00)
        Menu.objects.create(name="Test menu 3", restaurant=restaurant2, price=200.00)

        request_data = {
            "restaurant_id": restaurant1.id
        }

        response = self.client.post(reverse("create-vote"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request_data["restaurant_id"] = restaurant2.id

        response = self.client.post(reverse("create-vote"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)