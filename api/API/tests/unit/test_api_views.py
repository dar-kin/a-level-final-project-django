from datetime import date
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from customuser.models import MyUser
from cinema.models import Session, BookedSession


class TestListSessionsPlaces(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = MyUser.objects.get(id=2)
        self.session = Session.objects.get(id=2)
        self.booked_session = Session.objects.get(id=1)

    def test_places_number(self):
        print(self.session.booked_sessions.all())
        self.client.force_login(self.user)
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 4)]))
        data = response.data
        self.assertEqual(0, data[0]["free_places"])

    def test_places_number1(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 4)]))
        data = response.data
        self.assertEqual(0, data[1]["free_places"])

    def test_places_number2(self):
        session = Session.objects.get(id=3)
        BookedSession.objects.create(user=self.user, session=session, date=date(2021, 10, 4), places=2)
        self.client.force_login(self.user)
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 4)]))
        data = response.data
        self.assertEqual(1, data[2]["free_places"])
