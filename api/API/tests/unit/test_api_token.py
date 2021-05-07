from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from api.models import ExpiringToken
from customuser.models import MyUser
from rest_framework.test import APIClient
from api.misc import ExpiringTokenAuthentication


class ExpiringTokenModel(TestCase):
    fixtures = ["fixtures/users.json"]

    def setUp(self) -> None:
        self.user = MyUser.objects.get(id=1)

    def test_create_token_last_action(self):
        token = ExpiringToken.objects.create(user=self.user)
        self.assertEqual(timezone.now().strftime("%M:%S"), token.last_action.strftime("%M:%S"))


class TestExpiringTokenAuth(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = MyUser.objects.create_user(username="darkin", password="1", is_superuser=True)
        response = self.client.post("/api-token-auth/", data={"username": "darkin", "password": 1}, format="json")
        self.res_user, self.token = ExpiringTokenAuthentication().authenticate_credentials(response.data["token"])

    def test_auth_user(self):
        self.assertEqual(self.user, self.res_user)

    def test_auth_token(self):
        self.assertEqual(self.token, ExpiringToken.objects.get(user=self.user))

    def test_incorrect_user(self):
        response = self.client.post("/api-token-auth/", data={"username": "darkin1", "password": 1}, format="json")
        self.assertEqual("incorrect credentials", response.data["fail_message"])

    def test_token_cred(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(reverse("api:session-list"))
        self.assertEqual(200, response.status_code)
