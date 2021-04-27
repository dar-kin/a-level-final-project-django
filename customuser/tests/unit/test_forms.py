from customuser.forms import MyUserCreationForm
from customuser.models import MyUser
from django.test import TestCase


class TestMyUserFrom(TestCase):
    def setUp(self) -> None:
        MyUser.objects.create_user(username="user", password="123")
        self.incorrect_username_form = MyUserCreationForm(data={"username": "user", "password1": "123abcde",
                                                                "password2": '123abcde'})
        self.incorrect_password_form = MyUserCreationForm(data={"username": "user2", "password1": [], "password2": []})
        self.correct_form = MyUserCreationForm(data={"username": "user3", "password1": "123abcde",
                                                     "password2": "123abcde"})
        self.password_mismatch_form = MyUserCreationForm(data={"username": "user1234", "password1": "123abcde1",
                                                               "password2": "123abcde"})

    def test_incorrect_username_form(self):
        self.assertFalse(self.incorrect_username_form.is_valid())

    def test_incorrect_password_form(self):
        self.assertFalse(self.incorrect_password_form.is_valid())

    def test_correct_form(self):
        self.correct_form.is_valid()
        self.assertTrue(self.correct_form.is_valid())

    def test_form_save(self):
        self.correct_form.save()
        user = MyUser.objects.get(username="user3")
        self.assertEqual("user3", user.username)

    def test_password_mismatch_form(self):
        self.assertFalse(self.password_mismatch_form.is_valid())