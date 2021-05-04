from django.test import TestCase
from django.urls import reverse
from cinema.models import Hall
from customuser.models import MyUser
from rest_framework.test import APIClient
from api.API.serializers import HallSerializer


class TestCreateHall(TestCase):
    fixtures = ["fixtures/users.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)
        hall = Hall.objects.create(name="hall1", size=10)
        self.correct_data = {"name": "hall", "size": 10}
        self.correct_data3 = {"name": "hall4", "size": 10}
        self.incorrect_size_data = {"name": "hall", "size": -10}
        self.incorrect_name_data = {"name": "hall1", "size": 10}

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("api:hall-list"))
        self.assertEqual(403, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("api:hall-list"))
        self.assertEqual(403, response.status_code)

    def test_not_super_user_not_allowed_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("api:hall-list"), self.correct_data)
        self.assertEqual(403, response.status_code)

    def test_not_super_user_not_allowed_post_message(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("api:hall-list"), self.correct_data)
        error = "You do not have permission to perform this action."
        self.assertEqual(error, response.data["detail"])

    def test_unique_name(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("api:hall-list"), self.incorrect_name_data)
        error = "hall with this name already exists."
        self.assertEqual(error, response.data["name"][0])

    def test_negative_size(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("api:hall-list"), self.incorrect_size_data)
        error = "Ensure this value is greater than or equal to 0."
        self.assertEqual(error, response.data["size"][0])

    def test_hall_is_actually_created(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("api:hall-list"), self.correct_data)
        self.assertEqual("hall", Hall.objects.get(id=2).name)

    def test_success_message(self):
        self.client.force_login(self.s_user)
        response = self.client.post(reverse("api:hall-list"), self.correct_data3)
        message = "Hall was created"
        self.assertEqual(message, response.data["success_message"])


class TestUpdateHall(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json",
                "fixtures/booked_sessions.json"]

    def setUp(self) -> None:
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)
        self.client = APIClient()
        self.correct_data = {"name": "hall123", "size": 10}
        self.correct_data3 = {"name": "hall125", "size": 10}
        self.incorrect_size_data = {"name": "hall110", "size": -10}
        self.incorrect_name_data = {"name": "hall2", "size": 10}

    def test_unathorized_not_allowed(self):
        response = self.client.put(reverse("api:hall-detail", args=[1]), self.correct_data)
        self.assertEqual(403, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.put(reverse("api:hall-detail", args=[1]), self.correct_data)
        self.assertEqual(403, response.status_code)

    def test_unique_name(self):
        self.client.force_login(self.s_user)
        response = self.client.put(reverse("api:hall-detail", args=[1]), self.incorrect_name_data)
        error = "hall with this name already exists."
        self.assertEqual(error, response.data["name"][0])

    def test_negative_size(self):
        self.client.force_login(self.s_user)
        response = self.client.put(reverse("api:hall-detail", args=[1]), self.incorrect_size_data)
        error = "Ensure this value is greater than or equal to 0."
        self.assertEqual(error, response.data["size"][0])

    def test_hall_is_actually_updated(self):
        self.client.force_login(self.s_user)
        response = self.client.put(reverse("api:hall-detail", args=[1]), self.correct_data)
        self.assertEqual("hall123", Hall.objects.get(id=1).name)

    def test_success_message(self):
        self.client.force_login(self.s_user)
        response = self.client.put(reverse("api:hall-detail", args=[1]), self.correct_data3)
        message = "Hall was updated"
        self.assertEqual(message, response.data["success_message"])

    def test_update_fail_to_hall_with_booked_session(self):
        self.client.force_login(self.s_user)
        response = self.client.put(reverse("api:hall-detail", args=[2]), self.correct_data3)
        self.assertEqual(400, response.status_code)

    def test_update_fail_to_hall_with_booked_session_message(self):
        self.client.force_login(self.s_user)
        response = self.client.put(reverse("api:hall-detail", args=[2]), self.correct_data3)
        message = "Booked sessions for this hall exist"
        self.assertEqual(message, response.data["fail_message"])


class TestHallList(TestCase):
    fixtures = ["fixtures/users.json", "fixtures/halls.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.s_user = MyUser.objects.get(id=1)
        self.user = MyUser.objects.get(id=2)

    def test_unathorized_not_allowed(self):
        response = self.client.get(reverse("api:hall-list"))
        self.assertEqual(403, response.status_code)

    def test_not_superuser_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("api:hall-list"))
        self.assertEqual(403, response.status_code)

    def test_hall_list(self):
        halls = Hall.objects.all()
        serializer = HallSerializer(halls, many=True)
        self.client.force_login(self.s_user)
        response = self.client.get(reverse("api:hall-list"))
        self.assertQuerysetEqual(serializer.data, response.data)