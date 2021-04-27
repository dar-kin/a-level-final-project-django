from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.db.models import ObjectDoesNotExist
from cinema.models import Hall, Session, BookedSession
from customuser.models import MyUser


class TestBookedSession(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.user = MyUser.objects.get(id=2)
        self.session = Session.objects.get(id=1)
        self.no_free_places = {"user": 1, "session": 1, "places": 1, "date": "2021-10-4"}
        self.correct_data = {"user": 1, "session": 1, "places": 1, "date": "2021-10-5"}
        self.correct_data2 = {"user": 1, "session": 1, "places": 1, "date": "2021-10-5"}
        self.correct_data3 = {"user": 1, "session": 1, "places": 1, "date": "2021-10-5"}

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("cinema:booksession", args=[self.session, date(2021, 10, 5)]))
        self.assertRedirects(response, reverse("customuser:login") + "?next=/cinema/booksession/1/2021-10-05/")

    def test_no_free_places_error_message(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 4)]), follow=True)
        messages = response.context["messages"]
        message = "No free places"
        self.assertEqual(message, str(list(messages)[0]))

    def test_no_free_places_error_template(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession"), self.no_free_places, follow=True)
        self.assertTemplateUsed(response, "create_booked_session.html")

    def test_no_free_places_not_created(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession"), self.no_free_places)
        with self.assertRaises(ObjectDoesNotExist):
            BookedSession.objects.get(id=4)

    def test_correct_creation(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession"), self.correct_data, follow=True)
        session = BookedSession.objects.get(id=4)
        self.assertTrue(session)

    def test_correct_creation_message(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession"), self.correct_data2, follow=True)
        messages = response.context["messages"]
        message = "Session was booked"
        self.assertEqual(message, str(list(messages)[0]))

    def test_correct_creation_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession"), self.correct_data2, follow=True)
        self.assertRedirects(response, "/")
