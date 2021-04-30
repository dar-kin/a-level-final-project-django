from datetime import date, time
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


class TestFormIsValid(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json"]

    def setUp(self) -> None:
        self.user = MyUser.objects.get(id=2)
        self.session = Session.objects.get(id=2)
        self.client.force_login(self.user)
        self.client.post(reverse("cinema:booksession", args=[self.session, date(2021, 10, 4)]),
                         data={"places": 1})

    def test_is_created(self):
        self.assertTrue(BookedSession.objects.get(id=1))

    def test_correct_created_session(self):
        self.assertTrue(self.session, BookedSession.objects.get(id=1).session)

    def test_correct_created_user(self):
        self.assertTrue(self.user, BookedSession.objects.get(id=1).user)

    def test_correct_created_date(self):
        self.assertTrue(date(2021, 10, 4), BookedSession.objects.get(id=1).date)

    def test_correct_created_places(self):
        self.assertTrue(1, BookedSession.objects.get(id=1).places)


class TestUserSessionListContextData(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/user_session_list.json"]

    def setUp(self) -> None:
        self.user = MyUser.objects.get(id=1)

    def test_correct_data_in_url(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 10, 3)]))
        sessions = response.context_data["object_list"]
        self.assertQuerysetEqual(Session.objects.filter(start_date__lte=date(2021, 10, 3),
                                                        end_date__gte=date(2021, 10, 3)), sessions, ordered=False)

    def test_correct_data_in_url1(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 11, 3)]))
        sessions = response.context_data["object_list"]
        self.assertQuerysetEqual(Session.objects.filter(start_date__lte=date(2021, 11, 3),
                                                        end_date__gte=date(2021, 11, 3)), sessions, ordered=False)

    def test_correct_object_count(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 11, 3)]))
        sessions = response.context_data["object_list"]
        self.assertEqual(1, len(sessions))

    def test_correct_data_in_url2(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 10, 4)]))
        sessions = response.context_data["object_list"]
        self.assertQuerysetEqual(Session.objects.filter(start_date__lte=date(2021, 10, 4),
                                                        end_date__gte=date(2021, 10, 4)), sessions, ordered=False)

    def test_correct_object_count1(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 10, 4)]))
        sessions = response.context_data["object_list"]
        self.assertEqual(4, len(sessions))

    def test_no_sessions(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 9, 4)]))
        sessions = response.context_data["object_list"]
        self.assertEqual(0, len(sessions))

    def test_no_sessions1(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 10, 2)]))
        sessions = response.context_data["object_list"]
        self.assertEqual(0, len(sessions))

    def test_correct_sort_by_time(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 10, 4), "start_time"]))
        sessions = response.context_data["object_list"]
        expected = Session.objects.filter(start_date__lte=date(2021, 10, 4),
                                          end_date__gte=date(2021, 10, 4)).order_by("start_time")
        self.assertQuerysetEqual(expected, sessions)

    def test_correct_sort_by_price(self):
        response = self.client.get(reverse("cinema:clientsessionlist", args=[date(2021, 10, 4), "price"]))
        sessions = response.context_data["object_list"]
        expected = Session.objects.filter(start_date__lte=date(2021, 10, 4),
                                          end_date__gte=date(2021, 10, 4)).order_by("price")
        self.assertQuerysetEqual(expected, sessions)


class TestBookedSessionListContextData(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.user = MyUser.objects.get(id=1)
        self.user2 = MyUser.objects.get(id=2)
        self.user3 = MyUser.objects.get(id=3)

    def test_correct_total_money_spent(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cinema:bookedsessionlist"))
        money_spent = response.context_data["total_spent"]
        self.assertEqual(30, money_spent)

    def test_correct_total_money_spent2(self):
        self.client.force_login(self.user3)
        response = self.client.get(reverse("cinema:bookedsessionlist"))
        money_spent = response.context_data["total_spent"]
        self.assertEqual(30, money_spent)

    def test_correct_object_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cinema:bookedsessionlist"))
        sessions = response.context_data["object_list"]
        expected = BookedSession.objects.filter(user=self.user)
        self.assertQuerysetEqual(expected, sessions, ordered=False)

    def test_correct_zero_spent(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse("cinema:bookedsessionlist"))
        money_spent = response.context_data["total_spent"]
        self.assertEqual(0, money_spent)

    def test_correct_empty_object_list(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse("cinema:bookedsessionlist"))
        sessions = response.context_data["object_list"]
        self.assertEqual(0, len(sessions))