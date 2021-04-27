from django.test import TestCase
from customuser.models import MyUser
from django.core.exceptions import ValidationError


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.incorrect_user_wallet = MyUser(username="user", password="1", wallet=-10)
        self.correct_user_wallet = MyUser(username="user13", password="1", wallet=100)
        self.zero_user_wallet = MyUser(username="zero", password="1", wallet=0)
        self.generated_user_wallet = MyUser(username="user2", password="1")

    def test_incorrect_user_password(self):
        with self.assertRaises(TypeError):
            self.incorrect_user_password = MyUser.objects.create_user(username="user45", password=1)

    def test_incorrect_user_wallet(self):
        with self.assertRaises(ValidationError):
            self.incorrect_user_wallet.full_clean()

    def test_zero_user_wallet(self):
        self.zero_user_wallet.save()
        user = MyUser.objects.get(username="zero")
        self.assertEqual(0, user.wallet)

    def test_correct_user_wallet(self):
        self.correct_user_wallet.save()
        user = MyUser.objects.get(username="user13")
        self.assertEqual(100, user.wallet)

    def test_generated_wallet(self):
        self.generated_user_wallet.save()
        user = MyUser.objects.get(username="user2")
        self.assertEqual(10000, user.wallet)
