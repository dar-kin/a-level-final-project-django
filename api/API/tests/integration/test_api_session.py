from datetime import time
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from cinema.models import Hall, Session
from customuser.models import MyUser
from api.API.serializers import SessionSerializer


def create_data(start_time, end_time, start_date, end_date, hall, price):
    return {"start_time": start_time, "end_time": end_time,
            "start_date": start_date, "end_date": end_date,
            "hall": hall, "price": price}


class TestCreateSession(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        hall = Hall.objects.get(id=2)
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)
        self.collide_data = create_data("10:30", "13:00", "2021-9-20", "2021-10-6", 2, 10)
        self.random_data = create_data("fsfs", "13:00", "2021-9-20", "2021-10-6", 2, 10)
        self.incorret_range_data = create_data("9:00", "13:00", "2021-9-20", "2021-8-6", 2, 10)
        self.past_session = create_data("9:00", "13:00", "2020-9-20", "2020-8-6", 2, 10)
        self.correct_session = create_data("9:00", "13:00", "2021-7-18", "2021-7-21", 2, 10)
        self.correct_session3 = create_data("18:00", "19:00", "2021-7-20", "2021-7-21", 2, 10)

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("api:session-list"))
        self.assertEqual(401, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("api:session-list"))
        self.assertEqual(403, response.status_code)

    def test_not_super_user_not_allowed_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("api:session-list"), self.collide_data)
        self.assertEqual(403, response.status_code)

    def test_collide_data(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.post(reverse("api:session-list"), self.collide_data)
        message = "Session collides with another one"
        self.assertEqual(message, response.data["fail_message"])

    def test_incorrect_data(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.post(reverse("api:session-list"), self.random_data)
        self.assertEqual(400, response.status_code)

    def test_incorrect_range_data(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.post(reverse("api:session-list"), self.incorret_range_data)
        error = "Incorrect date"
        self.assertEqual(error, response.data["non_field_errors"][0])

    def test_past_session(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.post(reverse("api:session-list"), self.past_session)
        error = "Incorrect date"
        self.assertEqual(error, response.data["non_field_errors"][0])

    def test_session_is_created(self):
        self.client.force_authenticate(self.s_user)
        self.client.post(reverse("api:session-list"), self.correct_session3)
        self.assertTrue(Session.objects.get(id=4))

    def test_success_message(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.post(reverse("api:session-list"), self.correct_session)
        message = "Session was created"
        self.assertEqual(message, response.data["success_message"])


class TestUpdateSession(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        hall = Hall.objects.get(id=2)
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)
        self.collide_data = create_data("10:30", "13:00", "2021-9-20", "2021-10-6", 2, 10)
        self.client = APIClient()
        self.incorret_range_data = create_data("9:00", "13:00", "2021-9-20", "2021-8-6", 2, 10)
        self.past_session = create_data("9:00", "13:00", "2020-9-20", "2020-8-6", 2, 10)
        self.correct_session = create_data("9:00", "13:00", "2021-7-18", "2021-7-21", 2, 10)
        self.correct_session2 = create_data("14:00", "17:00", "2021-7-20", "2021-7-21", 2, 10)
        self.correct_session3 = create_data("18:00", "19:00", "2021-7-20", "2021-7-21", 2, 10)

    def test_unathorized_not_allowed(self):
        response = self.client.put(reverse("api:session-detail", args=[1]))
        self.assertEqual(401, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(reverse("api:session-detail", args=[1]))
        self.assertEqual(403, response.status_code)

    def test_not_super_user_not_allowed_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(reverse("api:session-detail", args=[1]), self.collide_data)
        self.assertEqual(403, response.status_code)

    def test_collide_data(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.put(reverse("api:session-detail", args=[3]), self.collide_data)
        message = "Session collides with another one"
        self.assertEqual(message, response.data["fail_message"])

    def test_incorrect_range_data(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.put(reverse("api:session-detail", args=[3]), self.incorret_range_data)
        error = "Incorrect date"
        self.assertEqual(error, response.data["non_field_errors"][0])

    def test_past_session(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.put(reverse("api:session-detail", args=[3]), self.past_session)
        error = "Incorrect date"
        self.assertEqual(error, response.data["non_field_errors"][0])

    def test_booked_session_exist(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.put(reverse("api:session-detail", args=[1]), self.correct_session)
        message = "Booked sessions for this session exist"
        self.assertEqual(message, response.data["fail_message"])

    def test_session_is_update(self):
        self.client.force_authenticate(self.s_user)
        self.client.put(reverse("api:session-detail", args=[3]), self.correct_session3)
        self.assertEqual(time(18), Session.objects.get(id=3).start_time)

    def test_success_message(self):
        self.client.force_authenticate(self.s_user)
        response = self.client.put(reverse("api:session-detail", args=[3]), self.correct_session, follow=True)
        message = "Session was updated"
        self.assertEqual(message, response.data["success_message"])


class TestSessionList(TestCase):
    fixtures = ["fixtures/users.json", "fixtures/halls.json", "fixtures/sessions.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("api:session-list"))
        self.assertEqual(401, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("api:session-list"))
        self.assertEqual(403, response.status_code)

    def test_hall_list(self):
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        self.client.force_authenticate(self.s_user)
        response = self.client.get(reverse("api:session-list"))
        self.assertQuerysetEqual(serializer.data, response.data)