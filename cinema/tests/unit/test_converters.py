from django.test import TestCase
from datetime import date
from cinema.misc import DateConverter, SessionConverter
from cinema.models import Session


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

