from datetime import date
from django.test import TestCase
from cinema.templatetags.alter_date import plus_days, current_date


class TestDateFilter(TestCase):
    def test_correct_data(self):
        self.assertEqual(date(2021, 10, 5), plus_days(date(2021, 10, 4), 1))

    def test_correct_data1(self):
        self.assertEqual(date(2021, 11, 1), plus_days(date(2021, 10, 31), 1))

    def test_correct_data2(self):
        self.assertEqual(date(2021, 11, 11), plus_days(date(2021, 10, 31), 11))


class TestCurrentDateTag(TestCase):
    def test_current_date_tag(self):
        self.assertEqual(date.today(), current_date())
