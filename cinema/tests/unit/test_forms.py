from django.test import TestCase
from cinema.models import Hall, Session
from customuser.models import MyUser
from cinema.forms import HallForm, SessionForm, BookedSessionForm


class TestHallForm(TestCase):
    def setUp(self) -> None:
        self.hall = Hall.objects.create(name="hall", size=10)
        self.incorrect_form_unique = HallForm(data={"name": "hall", "size": 10})
        self.incorrect_form_size = HallForm(data={"name": "hall1", "size": -10})
        self.correct_form = HallForm(data={"name": "hall1", "size": 10})

    def test_incorrect_form_unique(self):
        self.assertFalse(self.incorrect_form_unique.is_valid())

    def test_incorrect_form_size(self):
        self.assertFalse(self.incorrect_form_size.is_valid())

    def test_correct_form(self):
        self.assertTrue(self.correct_form.is_valid())

    def test_correct_form_save(self):
        self.correct_form.save()
        hall = Hall.objects.get(name="hall1")
        self.assertEqual("hall1", hall.name)


class TestSessionForm(TestCase):

    def create_form(self, start_time, end_time, start_date, end_date, hall, price):
        return SessionForm(data={"start_time": start_time, "end_time": end_time,
                                 "start_date": start_date, "end_date": end_date,
                                 "hall": hall, "price": price})

    def setUp(self) -> None:
        self.hall1 = Hall.objects.create(name="hall1", size=10)
        self.hall2 = Hall.objects.create(name="hall2", size=10)
        self.incorrect_form1 = self.create_form("12:30", "14:30", "2021-10-3", "2021-10-2", self.hall1, 10)
        self.incorrect_form2 = self.create_form("12:30", "11:00", "2021-10-3", "2021-10-3", self.hall1, 10)
        self.incorrect_form3 = self.create_form("12:30", "13:00", "2021-1-3", "2021-1-10", self.hall1, 10)
        self.correct_form = self.create_form("12:30", "13:00", "2021-10-3", "2021-10-3", self.hall1, 10)
        self.correct_form1 = self.create_form("12:30", "13:00", "2021-10-3", "2021-10-5", self.hall1, 10)

    def test_incorrect_form(self):
        self.assertFalse(self.incorrect_form1.is_valid())

    def test_incorrect_form1(self):
        self.assertFalse(self.incorrect_form3.is_valid())

    def test_incorrect_form_error(self):
        self.assertFalse(self.incorrect_form3.is_valid())
        error = "Incorrect date"
        self.assertEqual(error, self.incorrect_form3._errors["__all__"][0])

    def test_incorrect_form_error_message(self):
        self.incorrect_form1.is_valid()
        error = "Incorrect date"
        self.assertEqual(error, self.incorrect_form1._errors["__all__"][0])

    def test_incorrect_form2(self):
        self.assertFalse(self.incorrect_form1.is_valid())

    def test_incorrect_form1_error_message(self):
        self.incorrect_form1.is_valid()
        error = "Incorrect date"
        self.assertEqual(error, self.incorrect_form1._errors["__all__"][0])

    def test_correct_form(self):
        self.assertTrue(self.correct_form.is_valid())

    def test_correct_form1(self):
        self.assertTrue(self.correct_form.is_valid())


class TestBookedSessionForm(TestCase):
    fixtures = ["fixtures/users.json",
                "fixtures/halls.json",
                "fixtures/sessions.json"]

    def test_min_value_validator(self):
        form = BookedSessionForm(data={"places": 0})
        form.is_valid()
        error = "Ensure this value is greater than or equal to 1."
        self.assertEqual(error, form._errors["places"][0])
