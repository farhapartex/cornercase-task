from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from user.enums import RoleChoices
from restaurant.models import Restaurant, Menu


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


class MenuCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_admin = User.objects.create(username="dev1@test.com", email="dev1@test.com",
                                              role=RoleChoices.ADMIN.value)
        self.user_admin.set_password("Test123")
        self.user_employee = User.objects.create(username="dev2@test.com", email="dev2@test.com",
                                                 role=RoleChoices.EMPLOYEE.value)
        self.user_employee.set_password("Test123")
        self.user_owner1 = User.objects.create(username="dev3@test.com", email="dev3@test.com",
                                              role=RoleChoices.OWNER.value)
        self.user_owner1.set_password("Test123")
        self.user_owner2 = User.objects.create(username="dev4@test.com", email="dev4@test.com",
                                              role=RoleChoices.OWNER.value)
        self.user_owner2.set_password("Test123")

    def test_api_get_method(self):
        self.client.force_authenticate(user=self.user_owner1)
        response = self.client.get(reverse("create-menu"), format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_menu_create_by_owner(self):
        """
        1. A owner is able to create menu only for his own restaurant
        :return:
        """
        self.client.force_authenticate(user=self.user_owner1)
        restaurant1 = Restaurant.objects.create(owner=self.user_owner1, name="Test Restaurant 1")

        # restaurant id is missing, bad request
        request_data = {
            "name": "Vegitable",
            "price": 20.00
        }
        response = self.client.post(reverse("create-menu"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # restaurant id wrong, not exists
        request_data = {
            "name": "Vegitable",
            "restaurant_id": 102,
            "price": 20.00
        }
        response = self.client.post(reverse("create-menu"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_data = {
            "name": "Vegitable",
            "restaurant_id": restaurant1.id,
            "price": 20.00
        }
        response = self.client.post(reverse("create-menu"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(restaurant1.menus.all().count(), 1)

    def test_api_menu_create_by_admin(self):
        """
        A admin is able to create menu for any restaurant
        :return:
        """
        self.client.force_authenticate(user=self.user_admin)
        restaurant1 = Restaurant.objects.create(owner=self.user_owner1, name="Test Restaurant 1")

        request_data = {
            "name": "Vegitable",
            "restaurant_id": restaurant1.id,
            "price": 20.00
        }
        response = self.client.post(reverse("create-menu"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_menu_create_by_employee(self):
        """
        A employee is able to create menu for any restaurant
        :return:
        """
        self.client.force_authenticate(user=self.user_employee)
        restaurant1 = Restaurant.objects.create(owner=self.user_owner1, name="Test Restaurant 1")

        request_data = {
            "name": "Vegitable",
            "restaurant_id": restaurant1.id,
            "price": 20.00
        }
        response = self.client.post(reverse("create-menu"), data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MenuListTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_admin = User.objects.create(username="dev1@test.com", email="dev1@test.com",
                                              role=RoleChoices.ADMIN.value)
        self.user_admin.set_password("Test123")
        self.user_employee = User.objects.create(username="dev2@test.com", email="dev2@test.com",
                                                 role=RoleChoices.EMPLOYEE.value)
        self.user_employee.set_password("Test123")
        self.user_owner1 = User.objects.create(username="dev3@test.com", email="dev3@test.com",
                                              role=RoleChoices.OWNER.value)
        self.user_owner1.set_password("Test123")
        self.user_owner2 = User.objects.create(username="dev4@test.com", email="dev4@test.com",
                                              role=RoleChoices.OWNER.value)
        self.user_owner2.set_password("Test123")

        restaurant1 = Restaurant.objects.create(owner=self.user_owner1, name="Test Restaurant 1")
        restaurant2 = Restaurant.objects.create(owner=self.user_owner2, name="Test Restaurant 1")

        Menu.objects.create(name="Test menu 1", restaurant=restaurant1, price=200.00)
        Menu.objects.create(name="Test menu 2", restaurant=restaurant2, price=200.00)
        Menu.objects.create(name="Test menu 3", restaurant=restaurant2, price=200.00)
        self.menu = Menu.objects.create(name="Test menu 4", restaurant=restaurant2, price=200.00)
        self.menu.created_at = datetime(2022,2,3)
        self.menu.save()

    def test_api_menu_list_by_employee(self):
        self.client.force_authenticate(user=self.user_employee)
        response = self.client.get(reverse("menu-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Menu.objects.filter(created_at__date=timezone.now().date()).count())

    def test_api_menu_list_with_filter(self):
        self.client.force_authenticate(user=self.user_employee)
        response = self.client.get(f"{reverse('menu-list')}?created_at=2022-02-03", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_api_menu_list_by_admin(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(reverse("menu-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_menu_list_by_owner(self):
        self.client.force_authenticate(user=self.user_owner1)
        response = self.client.get(reverse("menu-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)