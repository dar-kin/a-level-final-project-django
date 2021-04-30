from django.test import TestCase
from django.urls import reverse
from cinema.models import Hall
from customuser.models import MyUser


class TestCreateHall(TestCase):
    fixtures = ["fixtures/users.json"]

    def setUp(self) -> None:
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)
        hall = Hall.objects.create(name="hall1", size=10)
        self.correct_data = {"name": "hall", "size": 10}
        self.correct_data2 = {"name": "hall2", "size": 10}
        self.correct_data3 = {"name": "hall4", "size": 10}
        self.incorrect_size_data = {"name": "hall", "size": -10}
        self.incorrect_name_data = {"name": "hall1", "size": 10}

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("cinema:createhall"))
        self.assertEqual(403, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cinema:createhall"))
        self.assertEqual(403, response.status_code)

    def test_not_super_user_not_allowed_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:createhall"), self.correct_data)
        self.assertEqual(403, response.status_code)

    def test_unique_name(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createhall"), self.incorrect_name_data)
        error = "Hall with this Name already exists."
        self.assertFormError(response=response, form='form', field="name", errors=[error, ])

    def test_negative_size(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createhall"), self.incorrect_size_data)
        error = "Ensure this value is greater than or equal to 0."
        self.assertFormError(response=response, form='form', field="size", errors=[error, ])

    def test_message_not_raised(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createhall"), self.incorrect_size_data)
        messages = response.context["messages"]
        self.assertEqual(0, len(messages))

    def test_template_used(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createhall"), self.incorrect_size_data)
        self.assertTemplateUsed(response, "create_hall.html")

    def test_hall_is_actually_created(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createhall"), self.correct_data)
        self.assertEqual("hall", Hall.objects.get(id=2).name)

    def test_success_redirect(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createhall"), self.correct_data2)
        self.assertRedirects(response, '/')

    def test_success_message(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createhall"), self.correct_data3, follow=True)
        messages = response.context["messages"]
        message = "Hall was created"
        self.assertEqual(message, str(list(messages)[0]))


class TestUpdateHall(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)
        self.correct_data = {"name": "hall123", "size": 10}
        self.correct_data2 = {"name": "hall124", "size": 10}
        self.correct_data3 = {"name": "hall125", "size": 10}
        self.incorrect_size_data = {"name": "hall110", "size": -10}
        self.incorrect_name_data = {"name": "hall2", "size": 10}

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("cinema:updatehall", args=[1]))
        self.assertEqual(403, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cinema:updatehall", args=[1]))
        self.assertEqual(403, response.status_code)

    def test_not_super_user_not_allowed_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:updatehall", args=[1]), self.correct_data)
        self.assertEqual(403, response.status_code)

    def test_unique_name(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[1]), self.incorrect_name_data)
        error = "Hall with this Name already exists."
        self.assertFormError(response=response, form='form', field="name", errors=[error, ])

    def test_negative_size(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[1]), self.incorrect_size_data)
        error = "Ensure this value is greater than or equal to 0."
        self.assertFormError(response=response, form='form', field="size", errors=[error, ])

    def test_message_not_raised(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[1]), self.incorrect_size_data)
        messages = response.context["messages"]
        self.assertEqual(0, len(messages))

    def test_template_used(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[1]), self.incorrect_size_data)
        self.assertTemplateUsed(response, "update_hall.html")

    def test_hall_is_actually_updated(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[1]), self.correct_data)
        self.assertEqual("hall123", Hall.objects.get(id=1).name)

    def test_success_redirect(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[1]), self.correct_data2)
        self.assertRedirects(response, '/')

    def test_success_message(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[1]), self.correct_data3, follow=True)
        messages = response.context["messages"]
        message = "Hall was updated"
        self.assertEqual(message, str(list(messages)[0]))

    def test_update_fail_to_hall_with_booked_session(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[2]), self.correct_data3)
        self.assertEqual("hall2", Hall.objects.get(id=2).name)

    def test_update_fail_to_hall_with_booked_session_message(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatehall", args=[2]), self.correct_data3, follow=True)
        messages = response.context["messages"]
        message = "Booked sessions for this hall exist"
        self.assertEqual(message, str(list(messages)[0]))


class TestHallList(TestCase):
    fixtures = ["fixtures/users.json", "fixtures/halls.json"]

    def setUp(self) -> None:
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("cinema:halllist"))
        self.assertEqual(403, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cinema:halllist"))
        self.assertEqual(403, response.status_code)

    def test_hall_list(self):
        halls = Hall.objects.all()
        self.client.force_login(self.s_user)
        response = self.client.get(reverse("cinema:halllist"))
        self.assertQuerysetEqual(halls, response.context_data["object_list"], ordered=False)





