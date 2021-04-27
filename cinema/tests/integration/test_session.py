from datetime import time
from django.test import TestCase
from django.urls import reverse
from cinema.models import Hall, Session
from customuser.models import MyUser


class TestCreateSession(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json"]

    def create_data(self, start_time, end_time, start_date, end_date, hall, price):
        return {"start_time": start_time, "end_time": end_time,
                "start_date": start_date, "end_date": end_date,
                "hall": hall, "price": price}

    def setUp(self) -> None:
        hall = Hall.objects.get(id=2)
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)
        self.collide_data = self.create_data("10:30", "13:00", "2021-9-20", "2021-10-6", 2, 10)
        self.random_data = self.create_data("fsfs", "13:00", "2021-9-20", "2021-10-6", 2, 10)
        self.incorret_range_data = self.create_data("9:00", "13:00", "2021-9-20", "2021-8-6", 2, 10)
        self.past_session = self.create_data("9:00", "13:00", "2020-9-20", "2020-8-6", 2, 10)
        self.correct_session = self.create_data("9:00", "13:00", "2021-7-18", "2021-7-21", 2, 10)
        self.correct_session2 = self.create_data("14:00", "17:00", "2021-7-20", "2021-7-21", 2, 10)
        self.correct_session3 = self.create_data("18:00", "19:00", "2021-7-20", "2021-7-21", 2, 10)

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("cinema:createsession"))
        self.assertEqual(403, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cinema:createsession"))
        self.assertEqual(403, response.status_code)

    def test_not_super_user_not_allowed_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:createsession"), self.collide_data)
        self.assertEqual(403, response.status_code)

    def test_collide_data(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createsession"), self.collide_data, follow=True)
        messages = response.context["messages"]
        message = "Session collides with another one"
        self.assertEqual(message, str(list(messages)[0]))

    def test_collide_template(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createsession"), self.collide_data, follow=True)
        self.assertTemplateUsed(response, "create_session.html")

    def test_incorrect_data(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createsession"), self.random_data)
        error = "Enter a valid time."
        self.assertFormError(response, "form", "start_time", error)

    def test_incorrect_range_data(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createsession"), self.incorret_range_data)
        error = "Incorrect date"
        self.assertFormError(response, "form", "__all__", error)

    def test_past_session(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createsession"), self.past_session)
        error = "Incorrect date"
        self.assertFormError(response, "form", "__all__", error)

    def test_session_is_created(self):
        self.client.force_login(self.s_user)
        self.client.post(reverse("cinema:createsession"), self.correct_session3)
        self.assertTrue(Session.objects.get(id=4))

    def test_success_message(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createsession"), self.correct_session, follow=True)
        messages = response.context["messages"]
        message = "Session was created"
        self.assertEqual(message, str(list(messages)[0]))

    def test_success_redirect(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:createsession"), self.correct_session2)
        self.assertRedirects(response, "/")


class TestUpdateSession(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def create_data(self, start_time, end_time, start_date, end_date, hall, price):
        return {"start_time": start_time, "end_time": end_time,
                "start_date": start_date, "end_date": end_date,
                "hall": hall, "price": price}

    def setUp(self) -> None:
        hall = Hall.objects.get(id=2)
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)
        self.collide_data = self.create_data("10:30", "13:00", "2021-9-20", "2021-10-6", 2, 10)
        self.incorret_range_data = self.create_data("9:00", "13:00", "2021-9-20", "2021-8-6", 2, 10)
        self.past_session = self.create_data("9:00", "13:00", "2020-9-20", "2020-8-6", 2, 10)
        self.correct_session = self.create_data("9:00", "13:00", "2021-7-18", "2021-7-21", 2, 10)
        self.correct_session2 = self.create_data("14:00", "17:00", "2021-7-20", "2021-7-21", 2, 10)
        self.correct_session3 = self.create_data("18:00", "19:00", "2021-7-20", "2021-7-21", 2, 10)

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("cinema:updatesession", args=[1]))
        self.assertEqual(403, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cinema:updatesession", args=[1]))
        self.assertEqual(403, response.status_code)

    def test_not_super_user_not_allowed_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:updatesession", args=[1]), self.collide_data)
        self.assertEqual(403, response.status_code)

    def test_collide_data(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatesession", args=[3]), self.collide_data, follow=True)
        messages = response.context["messages"]
        message = "Session collides with another one"
        self.assertEqual(message, str(list(messages)[0]))

    def test_collide_template(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatesession", args=[3]), self.collide_data, follow=True)
        self.assertTemplateUsed(response, "update_session.html")

    def test_incorrect_range_data(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatesession", args=[3]), self.incorret_range_data)
        error = "Incorrect date"
        self.assertFormError(response, "form", "__all__", error)

    def test_past_session(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatesession", args=[3]), self.past_session)
        error = "Incorrect date"
        self.assertFormError(response, "form", "__all__", error)

    def test_booked_session_exist(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatesession", args=[1]), self.correct_session, follow=True)
        messages = response.context["messages"]
        message = "Booked sessions for this session exist"
        self.assertEqual(message, str(list(messages)[0]))

    def test_session_is_update(self):
        self.client.force_login(self.s_user)
        self.client.post(reverse("cinema:updatesession", args=[3]), self.correct_session3)
        self.assertEqual(time(18), Session.objects.get(id=3).start_time)

    def test_success_message(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatesession", args=[3]), self.correct_session, follow=True)
        messages = response.context["messages"]
        message = "Session was updated"
        self.assertEqual(message, str(list(messages)[0]))

    def test_success_redirect(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("cinema:updatesession", args=[3]), self.correct_session2)
        self.assertRedirects(response, "/")
