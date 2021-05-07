from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from customuser.models import MyUser


class TestRegistration(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.invalid_username_data = {"username": "darkin", "password": "1", "password2": "1"}
        self.password_mismatch_data = {"username": "darkin1", "password": "1", "password2": "2"}

        self.correct_data = {"username": "darkin1", "password": "1", "password2": "1"}
        self.correct_data1 = {"username": "darkin2", "password": "1", "password2": "1"}

    def test_invalid_create_with_username(self):
        response = self.client.post("/api/users/", self.invalid_username_data)
        self.assertEqual(400, response.status_code)

    def test_invalid_create_with_username_error(self):
        response = self.client.post("/api/users/", self.invalid_username_data)
        error = "A user with that username already exists."
        self.assertEqual(error, response.data["username"][0])

    def test_invalid_password(self):
        response = self.client.post("/api/users/", self.password_mismatch_data)
        self.assertEqual(400, response.status_code)

    def test_invalid_password_message(self):
        response = self.client.post("/api/users/", self.password_mismatch_data)
        error = "Passwords mismatch"
        self.assertEqual(error, response.data["non_field_errors"][0])

    def test_correct_creation(self):
        response = self.client.post("/api/users/", self.correct_data)
        self.assertTrue(MyUser.objects.get(username="darkin1"))

    def test_correct_message(self):
        response = self.client.post("/api/users/", self.correct_data)
        message = "User was registered"
        self.assertEqual(message, response.data["success_message"])

