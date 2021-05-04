from django.test import TestCase
from datetime import date, time
from cinema.misc import DateConverter, SessionConverter, TimeConverter, HallConverter
from cinema.models import Session, Hall


class TestDateConverter(TestCase):
    def setUp(self) -> None:
        self.date_converter = DateConverter()

    def test_incorrect_format(self):
        with self.assertRaises(ValueError):
            self.date_converter.to_python("wffsdsdf")

    def test_incorrect_date(self):
        with self.assertRaises(ValueError):
            self.date_converter.to_python("2021-14-10")

    def test_correct_date(self):
        self.assertEqual(date(2021, 10, 10), self.date_converter.to_python("2021-10-10"))

    def test_correct_url_transform(self):
        self.assertEqual("2021-10-10", self.date_converter.to_url(date(2021, 10, 10)))


class TestSessionConverter(TestCase):
    fixtures = ["fixtures/halls.json",
                "fixtures/sessions.json"]

    def setUp(self) -> None:
        self.session_converter = SessionConverter()

    def test_incorrect_data(self):
        with self.assertRaises(ValueError):
            self.session_converter.to_python("wffsdsdf")

    def test_not_existing_data(self):
        with self.assertRaises(ValueError):
            self.session_converter.to_python("4")

    def test_existing_session(self):
        session = self.session_converter.to_python("3")
        self.assertEqual(3, session.id)

    def test_transformation_to_url(self):
        session = Session.objects.get(id=1)
        self.assertEqual("1", self.session_converter.to_url(session))


class TestTimeConverter(TestCase):
    def setUp(self) -> None:
        self.time_converter = TimeConverter()

    def test_incorrect_format(self):
        with self.assertRaises(ValueError):
            self.time_converter.to_python("wffsdsdf")

    def test_incorrect_time(self):
        with self.assertRaises(ValueError):
            self.time_converter.to_python("36:00")

    def test_correct_time(self):
        self.assertEqual(time(10, 30), self.time_converter.to_python("10:30"))

    def test_correct_url_transform(self):
        self.assertEqual("10:30", self.time_converter.to_url(time(10, 30)))


class TestHallConverter(TestCase):
    fixtures = ["fixtures/halls.json"]

    def setUp(self) -> None:
        self.hall_converter = HallConverter()

    def test_incorrect_data(self):
        with self.assertRaises(ValueError):
            self.hall_converter.to_python("wffsdsdf")

    def test_not_existing_data(self):
        with self.assertRaises(ValueError):
            self.hall_converter.to_python("4")

    def test_existing_hall(self):
        hall = self.hall_converter.to_python("3")
        self.assertEqual(3, hall.id)

    def test_transformation_to_url(self):
        hall = Hall.objects.get(id=1)
        self.assertEqual("1", self.hall_converter.to_url(hall))

