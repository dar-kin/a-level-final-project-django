from django.test import TestCase
from cinema.models import Hall
from api.API import serializers


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
