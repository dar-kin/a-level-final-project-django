from datetime import date, time
from django.db.models import ObjectDoesNotExist
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from customuser.models import MyUser
from cinema.models import Session, BookedSession, Hall
from api.API.serializers import UserInfoBookedSessionsSerializer


class TestBookedSession(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = MyUser.objects.get(id=2)
        self.session = Session.objects.get(id=1)
        self.hall = Hall.objects.get(id=1)

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("api:create-booked-session", args=[self.session, date(2021, 10, 5)]))
        self.assertEqual(401, response.status_code)

    def test_no_free_places_error_message(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("api:create-booked-session", args=[self.session, date(2021, 10, 4)]),
                                    data={"places": 1}, follow=True)
        message = "Not enough free places"
        self.assertEqual(message, response.data["fail_message"])

    def test_no_free_places_not_created(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("api:create-booked-session", args=[self.session, date(2021, 10, 4)]),
                                    data={"places": 1}, follow=True)
        with self.assertRaises(ObjectDoesNotExist):
            BookedSession.objects.get(id=6)

    def test_correct_creation(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("api:create-booked-session", args=[self.session, date(2021, 10, 5)]),
                                    data={"places": 1}, follow=True)
        session = BookedSession.objects.get(id=6)
        self.assertTrue(session)

    def test_correct_creation_message(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("api:create-booked-session", args=[self.session, date(2021, 10, 5)]),
                                    data={"places": 1}, follow=True)
        message = "Session was booked"
        self.assertEqual(message, response.data["success_message"])

    def test_data_expired_message(self):
        session = Session.objects.create(start_time=time(10, 30), end_time=time(13, 20),
                                         start_date=date(2021, 5, 1), end_date=date(2021, 6, 1),
                                         hall=self.hall, price=16)
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("api:create-booked-session", args=[session, date(2021, 5, 4)]),
                                    data={"places": 1}, follow=True)
        message = "Date expired"
        self.assertEqual(message, response.data["fail_message"])


class TestBookedSessionList(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = MyUser.objects.get(id=1)
        self.user3 = MyUser.objects.get(id=3)
        self.user2 = MyUser.objects.get(id=2)

    def test_not_allowed_unathorized(self):
        response = self.client.get(reverse("api:my-booked-sessions"))
        self.assertEqual(401, response.status_code)

    def test_booked_session_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("api:my-booked-sessions"))
        booked_sessions = UserInfoBookedSessionsSerializer(BookedSession.objects.filter(user=self.user), many=True).data
        booked_sessions.append({"total_spent": 30})
        self.assertEqual(booked_sessions, response.data)

    def test_booked_session_list1(self):
        self.client.force_authenticate(self.user3)
        response = self.client.get(reverse("api:my-booked-sessions"))
        booked_sessions = UserInfoBookedSessionsSerializer(BookedSession.objects.filter(user=self.user3), many=True).data
        booked_sessions.append({"total_spent": 30})
        self.assertEqual(booked_sessions, response.data)

    def test_booked_session_list2(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(reverse("api:my-booked-sessions"))
        booked_sessions = UserInfoBookedSessionsSerializer(BookedSession.objects.filter(user=self.user2), many=True).data
        booked_sessions.append({"total_spent": 0})
        self.assertEqual(booked_sessions, response.data)