from django.urls import reverse
from django.test import TestCase
from .test_models import MyUser


class TestLogout(TestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="1")

    def test_logout_template(self):
        response = self.client.get(reverse("customuser:logout"))
        self.assertTemplateUsed(response, "logged_out.html")
