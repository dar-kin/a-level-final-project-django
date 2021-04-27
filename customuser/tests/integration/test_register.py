from django.test import TestCase
from django.urls import reverse
from customuser.models import MyUser


class TestRegister(TestCase):
    def setUp(self) -> None:
        self.correct_data = {"username": "user", "password1": "123abcde", "password2": "123abcde"}
        self.correct_data1 = {"username": "user1", "password1": "123abcde", "password2": "123abcde"}
        self.incorrect_data = {"username": "user", "password1": "123abcde", "password2": "123abde"}
        self.user = MyUser.objects.create_user(username="darkin", password="1")

    def test_template_used(self):
        response = self.client.get(reverse("customuser:register"))
        self.assertTemplateUsed(response, "register.html")

    def test_incorrect_data_response(self):
        response = self.client.post(reverse("customuser:register"), data=self.incorrect_data)
        error = "The two password fields didn’t match."
        self.assertFormError(response=response, form='form', field="password2", errors=[error, ])

    def test_correct_data_redirect(self):
        response = self.client.post(reverse("customuser:register"), data=self.correct_data)
        self.assertRedirects(response, reverse("customuser:login"))

    def test_user_creation(self):
        response = self.client.post(reverse("customuser:register"), data=self.correct_data1)
        user = MyUser.objects.get(username="user1")
        self.assertEqual("user1", user.username)


