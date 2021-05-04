from datetime import date
from django.test import TestCase
from cinema.models import Hall
from api.API import serializers
from customuser.models import MyUser


class TestHallForm(TestCase):
    def setUp(self) -> None:
        self.hall = Hall.objects.create(name="hall", size=10)
        self.incorrect_serializer_unique = serializers.HallSerializer(data={"name": "hall", "size": 10})
        self.incorrect_serializer_size = serializers.HallSerializer(data={"name": "hall1", "size": -10})
        self.correct_serializer = serializers.HallSerializer(data={"name": "hall1", "size": 10})

    def test_incorrect_serializer_unique(self):
        self.assertFalse(self.incorrect_serializer_unique.is_valid())

    def test_incorrect_serializer_size(self):
        self.assertFalse(self.incorrect_serializer_size.is_valid())

    def test_correct_serializer(self):
        self.assertTrue(self.correct_serializer.is_valid())

    def test_correct_serializer_save(self):
        self.correct_serializer.is_valid()
        self.correct_serializer.save()
        hall = Hall.objects.get(name="hall1")
        self.assertEqual("hall1", hall.name)


class TestSessionSerializer(TestCase):
    def create_serializer(self, start_time, end_time, start_date, end_date, hall, price):
        return serializers.SessionSerializer(data={"start_time": start_time, "end_time": end_time,
                                                   "start_date": start_date, "end_date": end_date,
                                                   "hall": hall, "price": price})

    def setUp(self) -> None:
        self.hall1 = Hall.objects.create(name="hall1", size=10)
        self.hall2 = Hall.objects.create(name="hall2", size=10)
        self.incorrect_serializer1 = self.create_serializer("12:30", "14:30", "2021-10-3", "2021-10-2", self.hall1.id, 10)
        self.incorrect_serializer2 = self.create_serializer("12:30", "11:00", "2021-10-3", "2021-10-3", self.hall1.id, 10)
        self.incorrect_serialiazer3 = self.create_serializer("12:30", "13:00", "2021-1-3", "2021-1-10", self.hall1.id, 10)
        self.correct_serializer = self.create_serializer("12:30", "13:00", "2021-10-3", "2021-10-3", self.hall1.id, 10)
        self.correct_serialzier1 = self.create_serializer("12:30", "13:00", "2021-10-3", "2021-10-5", self.hall1.id, 10)

    def test_incorrect_serialzier(self):
        self.assertFalse(self.incorrect_serializer1.is_valid())

    def test_incorrect_serialzier1(self):
        self.assertFalse(self.incorrect_serialiazer3.is_valid())

    def test_incorrect_serialzier3_error(self):
        self.incorrect_serialiazer3.is_valid()
        error = "Incorrect date"
        self.assertEqual(error, self.incorrect_serialiazer3.errors["non_field_errors"][0])

    def test_incorrect_serializer2(self):
        self.assertFalse(self.incorrect_serializer1.is_valid())

    def test_incorrect_serialzier2_error(self):
        self.incorrect_serializer2.is_valid()
        error = "Incorrect date"
        self.assertEqual(error, self.incorrect_serializer2.errors["non_field_errors"][0])

    def test_incorrect_serialzier1_error_message(self):
        self.incorrect_serializer1.is_valid()
        error = "Incorrect date"
        self.assertEqual(error, self.incorrect_serializer1.errors["non_field_errors"][0])

    def test_correct_serialzier(self):
        self.assertTrue(self.correct_serializer.is_valid())

    def test_correct_serialzier1(self):
        self.assertTrue(self.correct_serializer.is_valid())


class TestUserSerializer(TestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.incorrect_username_data = serializers.MyUserSerializer(data={"username": "darkin",
                                                                          "password": "1", "password2": "1"})
        self.password_mismatch_data = serializers.MyUserSerializer(data={"username": "darkin1",
                                                                         "password": "1", "password2": "2"})

        self.correct_serializer = serializers.MyUserSerializer(data={"username": "darkin1",
                                                               "password": "1", "password2": "1"})

        self.id_data = self.correct_serializer = serializers.MyUserSerializer(data={"id":10, "username": "darkin2",
                                                               "password": "1", "password2": "1"})

    def test_unique_username(self):
        error = "A user with that username already exists."
        self.incorrect_username_data.is_valid()
        self.assertEqual(error, self.incorrect_username_data.errors["username"][0])

    def test_password_mismatch(self):
        error = "Passwords mismatch"
        self.password_mismatch_data.is_valid()
        self.assertEqual(error, self.password_mismatch_data.errors["non_field_errors"][0])

    def test_correct_serializer(self):
        self.assertTrue(self.correct_serializer.is_valid())

    def test_password_write_only(self):
        self.assertFalse(serializers.MyUserSerializer(self.user).data.get("password", None))

    def test_password2_write_only(self):
        self.assertFalse(serializers.MyUserSerializer(self.user).data.get("password2", None))

    def test_id_read_only(self):
        self.id_data.is_valid()
        self.assertFalse(self.id_data.data.get("id", None))

    def test_user_is_created(self):
        self.correct_serializer.is_valid()
        user = self.correct_serializer.save()
        self.assertEqual(MyUser.objects.get(id=2), user)


class TestBookedSessionSerializer(TestCase):

    def test_min_value_validator(self):
        serializer = serializers.BookedSessionSerializer(data={"places": 0})
        serializer.is_valid()
        error = "Ensure this value is greater than or equal to 1."
        self.assertEqual(error, serializer.errors["places"][0])


class TestBookedSessionUserInfoSerialzier(TestCase):
    fixtures = ["fixtures/halls.json", "fixtures/sessions.json"]

    def setUp(self) -> None:
        self.incorrect_date_data = {"date": "adads", "places": 2, "session": 1}
        self.incorrect_session_data = {"date": date(2021, 10, 5), "places": 2, "session": 6}
        self.incorrect_places_data = {"date": date(2021, 10, 5), "places": -2, "session": 1}
        self.correct_data = {"date":  date(2021, 10, 5), "places": 2, "session": 1}

    def test_incorrect_date_data(self):
        serialzier = serializers.UserInfoBookedSessionsSerializer(data=self.incorrect_date_data)
        serialzier.is_valid()
        error = 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.'
        self.assertEqual(error, serialzier.errors["date"][0])

    def test_incorrect_session_data(self):
        serialzier = serializers.UserInfoBookedSessionsSerializer(data=self.incorrect_session_data)
        serialzier.is_valid()
        error = 'Invalid pk "6" - object does not exist.'
        self.assertEqual(error, serialzier.errors["session"][0])

    def test_incorrect_places_data(self):
        serialzier = serializers.UserInfoBookedSessionsSerializer(data=self.incorrect_places_data)
        serialzier.is_valid()
        error = 'Ensure this value is greater than or equal to 1.'
        self.assertEqual(error, serialzier.errors["places"][0])

    def test_correct_data(self):
        serialzier = serializers.UserInfoBookedSessionsSerializer(data=self.correct_data)
        self.assertTrue(serialzier.is_valid())

