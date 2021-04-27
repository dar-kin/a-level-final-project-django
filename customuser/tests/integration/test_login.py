from django.test import TestCase
from customuser.models import MyUser
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm


class TestLogin(TestCase):

    def setUp(self) -> None:
        self.correct_data = {"username": "darkin", "password": "1"}
        self.correct_data2 = {"username": "darkin1", "password": "1"}
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.user1 = MyUser.objects.create_user(username="darkin1", password="1")
        self.incorrect_data = {"username": "darki", "password": "1"}
        self.incorrect_data1 = {"username": "darkin", "password": "12"}
        self.random_data = {"data": 89, "lom": [], "ha": {}}

    def get_response(self, data):
        return self.client.post(reverse("customuser:login"), data)


    def test_incorrect_data_login(self):
        response = self.get_response(self.incorrect_data)
        error = "Please enter a correct username and password. Note that both fields may be case-sensitive."
        self.assertFormError(response=response, form='form', field="__all__", errors=[error, ])

    def test_incorrect_data_login1(self):
        response = self.get_response(self.incorrect_data1)
        error = "Please enter a correct username and password. Note that both fields may be case-sensitive."
        self.assertFormError(response=response, form='form', field="__all__", errors=[error, ])

    def test_incorrect_data_login_template(self):
        response = self.get_response(self.incorrect_data)
        self.assertTemplateUsed(response, "login.html")

    def test_incorrect_data_login_template1(self):
        response = self.get_response(self.incorrect_data)
        self.assertTemplateUsed(response, "login.html")

    def test_random_data_login(self):
        response = self.client.post(reverse("customuser:login"), self.random_data)
        self.assertTemplateUsed(response, "login.html")

    def test_correct_data_redirect(self):
        response = self.get_response(self.correct_data)
        self.assertRedirects(response, "/")

    def test_correct_data_redirect1(self):
        response = self.get_response(self.correct_data2)
        self.assertRedirects(response, "/")

    def test_redirect_auth_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("customuser:login"))
        self.assertRedirects(response, "/")


class TestMain(TestCase):
    def test_main_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "main.html")


