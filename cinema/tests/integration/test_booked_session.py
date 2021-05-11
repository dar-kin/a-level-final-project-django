from datetime import date, time
from django.test import TestCase
from django.urls import reverse
from django.db.models import ObjectDoesNotExist
from cinema.models import Session, BookedSession, Hall
from customuser.models import MyUser


class TestBookedSession(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.user = MyUser.objects.get(id=2)
        self.session = Session.objects.get(id=1)
        self.hall = Hall.objects.get(id=1)

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("cinema:booksession", args=[self.session, date(2021, 10, 5)]))
        self.assertRedirects(response, reverse("customuser:login") + "?next=/cinema/booksession/1/2021-10-05/")

    def test_no_free_places_error_message(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 4)]),
                                    data={"places": 1}, follow=True)
        messages = response.context["messages"]
        message = "No free places"
        self.assertEqual(message, str(list(messages)[0]))

    def test_date_expired_error(self):
        session = Session.objects.create(start_time=time(10, 30), end_time=time(13, 20),
                                         start_date=date(2021, 5, 1), end_date=date(2021, 6, 1),
                                         hall=self.hall, price=16)
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[session, date(2021, 5, 4)]),
                                    data={"places": 1}, follow=True)
        messages = response.context["messages"]
        message = "Date expired"
        self.assertEqual(message, str(list(messages)[0]))


    def test_no_free_places_error_template(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 4)]),
                                    data={"places": 1}, follow=True)
        self.assertTemplateUsed(response, "create_booked_session.html")

    def test_no_free_places_not_created(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 4)]),
                                    data={"places": 1}, follow=True)
        with self.assertRaises(ObjectDoesNotExist):
            BookedSession.objects.get(id=6)

    def test_not_enough_money_message(self):
        user = MyUser.objects.create_user(username="ppl", password="1", wallet=0)
        self.client.force_login(user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 10)]),
                                    data={"places": 1}, follow=True)
        messages = response.context["messages"]
        message = "Not enough money"
        self.assertEqual(message, str(list(messages)[0]))

    def test_correct_creation(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 5)]),
                                    data={"places": 1}, follow=True)
        session = BookedSession.objects.get(id=4)
        self.assertTrue(session)

    def test_correct_creation_message(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 5)]),
                                    data={"places": 1}, follow=True)
        messages = response.context["messages"]
        message = "Session was booked"
        self.assertEqual(message, str(list(messages)[0]))

    def test_correct_creation_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 5)]),
                                    data={"places": 1}, follow=True)
        self.assertRedirects(response, "/")

    def test_incorrect_data(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 5)]),
                                    data={"places": 1}, follow=True)
        self.assertRedirects(response, "/")


class TestBookedSessionList(TestCase):
    fixtures = ["fixtures/users.json"]

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("cinema:bookedsessionlist"))
        self.assertRedirects(response, reverse("customuser:login") + "?next=/cinema/bookedsessionlist/")

    def test_template_is_used(self):
        self.client.force_login(MyUser.objects.get(id=1))
        response = self.client.get(reverse("cinema:bookedsessionlist"))
        self.assertTemplateUsed(response, "booked_sessions_list.html")
