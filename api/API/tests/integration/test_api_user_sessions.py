from datetime import date, time
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from customuser.models import MyUser
from cinema.models import Session, Hall
from api.API.serializers import SessionSerializer


class TestUserSessionListContextData(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/user_session_list.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = MyUser.objects.get(id=1)

    def test_correct_data_in_url(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 3)]))
        sessions = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date(2021, 10, 3),
                                                            end_date__gte=date(2021, 10, 3)), many=True).data
        self.assertEqual(expected, sessions)

    def test_correct_data_in_url1(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 11, 3)]))
        sessions = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date(2021, 11, 3),
                                                            end_date__gte=date(2021, 11, 3)), many=True).data
        self.assertEqual(expected, sessions)

    def test_correct_object_count(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 11, 3)]))
        sessions = response.data
        self.assertEqual(1, len(sessions))

    def test_correct_data_in_url2(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 4)]))
        sessions = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date(2021, 10, 4),
                                                            end_date__gte=date(2021, 10, 4)), many=True).data
        self.assertEqual(expected, sessions)

    def test_correct_object_count1(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 4)]))
        sessions = response.data
        self.assertEqual(4, len(sessions))

    def test_no_sessions(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 9, 4)]))
        sessions = response.data
        self.assertEqual(0, len(sessions))

    def test_no_sessions1(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 2)]))
        sessions = response.data
        self.assertEqual(0, len(sessions))

    def test_correct_sort_by_time(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 4), "start_time"]))
        sessions = response.data
        expected = SessionSerializer(Session.objects.filter(
            start_date__lte=date(2021, 10, 4), end_date__gte=date(2021, 10, 4)).order_by("start_time"), many=True).data
        self.assertQuerysetEqual(expected, sessions)

    def test_correct_sort_by_price(self):
        response = self.client.get(reverse("api:clients-session-list", args=[date(2021, 10, 4), "price"]))
        sessions = response.data
        expected = SessionSerializer(Session.objects.filter(
            start_date__lte=date(2021, 10, 4), end_date__gte=date(2021, 10, 4)).order_by("price"), many=True).data
        self.assertEqual(expected, sessions)


class TestUserSessionsAction(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/particular_user_sessions.json"]

    def setUp(self) -> None:
        self.client = APIClient()

    def test_time_session_list(self):
        response = self.client.get(reverse("api:today-session-list", args=[time(0, 0), time(23)]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date.today(),
                                                            end_date__gte=date.today(),
                                                            start_time__gte=time(0, 0),
                                                            start_time__lte=time(23, 0)), many=True).data
        self.assertEqual(expected, data)

    def test_time_session_list1(self):
        response = self.client.get(reverse("api:today-session-list", args=[time(16), time(19)]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date.today(),
                                                            end_date__gte=date.today(),
                                                            start_time__gte=time(16),
                                                            start_time__lte=time(19)), many=True).data
        self.assertEqual(expected, data)

    def test_time_session_list2(self):
        response = self.client.get(reverse("api:today-session-list", args=[time(12), time(13)]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date.today(),
                                                            end_date__gte=date.today(),
                                                            start_time__gte=time(12),
                                                            start_time__lte=time(13)), many=True).data
        self.assertEqual(expected, data)


    def test_time_session_list3(self):
        response = self.client.get(reverse("api:today-session-list", args=[time(9), time(10)]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date.today(),
                                                            end_date__gte=date.today(),
                                                            start_time__gte=time(9),
                                                            start_time__lte=time(10)), many=True).data
        self.assertEqual(expected, data)

    def test_hall_session_list(self):
        hall = Hall.objects.get(id=2)
        response = self.client.get(reverse("api:today-session-list", args=[hall]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date.today(),
                                                            end_date__gte=date.today(),
                                                            hall=hall), many=True).data
        self.assertEqual(expected, data)

    def test_hall_session_list1(self):
        hall = Hall.objects.get(id=3)
        response = self.client.get(reverse("api:today-session-list", args=[hall]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(start_date__lte=date.today(),
                                                            end_date__gte=date.today(),
                                                            hall=hall), many=True).data
        self.assertEqual(expected, data)

    def test_hall_time_session_list(self):
        hall = Hall.objects.get(id=3)
        response = self.client.get(reverse("api:today-session-list", args=[hall]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(id=4), many=True).data
        self.assertEqual(expected, data)

    def test_hall_time_session_list1(self):
        hall = Hall.objects.get(id=3)
        response = self.client.get(reverse("api:today-session-list", args=[time(12), time(13), hall]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(id=4), many=True).data
        self.assertEqual(expected, data)

    def test_hall_time_session_list2(self):
        hall = Hall.objects.get(id=2)
        response = self.client.get(reverse("api:today-session-list", args=[time(12), time(13), hall]))
        data = response.data
        expected = SessionSerializer(Session.objects.filter(id=1), many=True).data
        self.assertEqual(expected, data)

