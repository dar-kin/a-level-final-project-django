from datetime import date
from django.test import TestCase, RequestFactory
from django.urls import reverse
from customuser.models import MyUser
from cinema.models import Session, BookedSession
from cinema.views import CreateBookedSessionView


class TestCreateBookedSessionView(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.user = MyUser.objects.get(id=2)
        self.session = Session.objects.get(id=2)
        self.factory = RequestFactory()
        self.booked_session = Session.objects.get(id=1)

    def test_context(self):
        self.client.force_login(self.user)
        request = self.client.get(path=reverse("cinema:booksession", args=[self.session, date(2021, 10, 5)]))
        context_data = request.context_data
        self.assertEqual(context_data["session"], self.session)

    def test_context2(self):
        self.client.force_login(self.user)
        request = self.client.get(path=reverse("cinema:booksession", args=[self.session, date(2021, 10, 5)]))
        context_data = request.context_data
        self.assertEqual(context_data["date"], date(2021, 10, 5))

    def test_context3(self):
        self.client.force_login(self.user)
        request = self.client.get(path=reverse("cinema:booksession", args=[self.booked_session, date(2021, 10, 4)]))
        context_data = request.context_data
        self.assertEqual(0, context_data["places"])

    def test_context4(self):
        self.client.force_login(self.user)
        request = self.client.get(path=reverse("cinema:booksession", args=[self.session, date(2021, 10, 4)]))
        context_data = request.context_data
        self.assertEqual(3, context_data["places"])

    def test_context5(self):
        BookedSession.objects.create(user=self.user, session=self.session, date=date(2021, 10, 4), places=2)
        self.client.force_login(self.user)
        request = self.client.get(path=reverse("cinema:booksession", args=[self.session, date(2021, 10, 4)]))
        context_data = request.context_data
        self.assertEqual(1, context_data["places"])
